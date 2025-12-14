import json
import os
from datetime import datetime, timedelta
from utils.data_manager import DataManager

RESERVATIONS_FILE = "reservations.json"

class ReservationManager:
    @staticmethod
    def _load_reservations():
        if not os.path.exists(RESERVATIONS_FILE):
            return []
        try:
            with open(RESERVATIONS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def _save_reservations(data):
        with open(RESERVATIONS_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def create_reservation(user_email, book_isbn, book_title):
        """
        Create a pending reservation if:
        1. User hasn't already reserved this book (pending).
        2. Book is actually unavailable (checked by caller mostly, but can add check here if we had book obj).
        """
        reservations = ReservationManager._load_reservations()
        
        # Check duplicates
        for res in reservations:
            if res['user_email'] == user_email and res['isbn'] == book_isbn and res['status'] == 'pending':
                return False, "You already have a pending reservation for this book."
        
        new_res = {
            "user_email": user_email,
            "isbn": book_isbn,
            "book_title": book_title,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
        }
        reservations.append(new_res)
        ReservationManager._save_reservations(reservations)
        return True, "Reservation placed successfully!"

    @staticmethod
    def get_user_reservations(user_email, status=None):
        reservations = ReservationManager._load_reservations()
        user_res = [r for r in reservations if r['user_email'] == user_email]
        if status:
            user_res = [r for r in user_res if r['status'] == status]
        return user_res

    @staticmethod
    def get_reservations_for_book(book_isbn):
        reservations = ReservationManager._load_reservations()
        # Return pending reservations sorted by date (though list is append-only, so naturally sorted)
        return [r for r in reservations if r['isbn'] == book_isbn and r['status'] == 'pending']

    @staticmethod
    def cancel_reservation(user_email, book_isbn):
        reservations = ReservationManager._load_reservations()
        for res in reservations:
            if res['user_email'] == user_email and res['isbn'] == book_isbn and res['status'] == 'pending':
                res['status'] = 'cancelled'
                ReservationManager._save_reservations(reservations)
                return True, "Reservation cancelled."
        return False, "Reservation not found or already processed."

    @staticmethod
    def process_return(book_isbn, book_obj):
        """
        Called when a book is returned.
        Checks if there are pending reservations.
        If yes:
          - Assign to first user (FIFO).
          - Create Loan immediately.
          - Mark reservation fulfilled.
          - DECREASE book quantity (since it goes from Returned -> Borrowed immediately).
          - RETURN string message about what happened.
        If no:
          - Just return "Available" (Caller will increment quantity).
        """
        pending = ReservationManager.get_reservations_for_book(book_isbn)
        
        if not pending:
            return None # No reservation logic triggered
            
        # FIFO : First one
        first_res = pending[0]
        user_email = first_res['user_email']
        
        # Fulfill reservation
        reservations = ReservationManager._load_reservations()
        for r in reservations:
            if r == first_res: # relying on dict equality or identity if loaded freshly? safer to match unique fields if possible
                # Match by email/isbn/date
                if r['user_email'] == user_email and r['isbn'] == book_isbn and r['date'] == first_res['date']:
                    r['status'] = 'fulfilled'
                    break
        ReservationManager._save_reservations(reservations)
        
        # Create Loan
        # Loan period 14 days
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        DataManager.add_loan(user_email, book_isbn, due_date)
        
        # Decrease quantity (Conceptually: User A returns -> Book ++ -> AutoAssign User B -> Book --. Net 0 change)
        if book_obj:
             book_obj.borrow()
        
        return f"Book automatically assigned to reserver: {user_email}"

    @staticmethod
    def update_status(user_email, book_isbn, new_status):
        reservations = ReservationManager._load_reservations()
        for res in reservations:
            if res['user_email'] == user_email and res['isbn'] == book_isbn and res['status'] == 'pending':
                res['status'] = new_status
                ReservationManager._save_reservations(reservations)
                return True
        return False
