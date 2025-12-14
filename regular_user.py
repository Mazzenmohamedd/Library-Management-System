from member import Member
from datetime import datetime, timedelta
from transaction import TransactionManager
from utils.reservation_manager import ReservationManager

class RegularUser(Member):
    LOAN_PERIOD_DAYS = 14
    FINE_PER_DAY = 10.0

    def __init__(self, user_id, name, age, email, password):
        super().__init__(user_id, name, age, email, password, role="user")
        self.reading_history = []
        self.favorites = []
        self.borrowed_books = []
        self.transaction_manager = TransactionManager()

    def borrow_book(self, book):
        if book.borrow():
            due_date = datetime.now() + timedelta(days=self.LOAN_PERIOD_DAYS)
            
        
            
            self.transaction_manager.log_transaction(self.email, book.isbn, "borrow")
            return True, f"Borrowed '{book.title}'. Due date: {due_date.strftime('%Y-%m-%d')}"
        else:
            return False, f"Sorry, '{book.title}' is not available."

    def return_book(self, book):
        from utils.data_manager import DataManager
        loans = DataManager.get_user_loans(self.email)
        
        borrowed_loan = next((l for l in loans if l['isbn'] == book.isbn), None)
        
        if not borrowed_loan:
            # Just in case persistence failed but book quantity was decremented
            # This is a safe-guard, but ideally shouldn't happen if flow is correct.
            # However, since view calls user.return_book BEFORE DataManager.remove_loan,
            # we should find it.
            return "Error: Loan record not found."

        book.return_book()
        # We do NOT remove from DataManager here, the View does it. 
        # But this separation ensures we calculate fine correctly.
        
        return_date = datetime.now()
        due_date = datetime.strptime(borrowed_loan['due_date'], "%Y-%m-%d")
        fine = 0.0
        
        if return_date > due_date:
            overdue_days = (return_date - due_date).days
            if overdue_days > 0:
                fine = overdue_days * self.FINE_PER_DAY
        
        history_record = {
            'title': book.title,
            'author': book.author,
            'return_date': return_date.strftime("%Y-%m-%d"),
            'fine': fine
        }
        
        # Add to persistent history
        DataManager.add_history(self.email, history_record)
        
        self.transaction_manager.log_transaction(self.email, book.isbn, "return")
        
        # Check for reservations and auto-assign
        assign_msg = ReservationManager.process_return(book.isbn, book)
        
        message = f"Returned '{book.title}'."
        
        if assign_msg:
             message += f" {assign_msg}"

        if fine > 0:
            message += f" Late return! Fine: {fine} LE."
            
        return message

    def check_due_dates(self):
        from utils.data_manager import DataManager
        alerts = []
        now = datetime.now()
        loans = DataManager.get_user_loans(self.email)
        
        for record in loans:
            try:
                # We need book title, but loan only has ISBN.
                # We'll fetch title from book manager or just use ISBN if title missing?
                # DataManager loans don't strictly store title in add_loan implementation in search.py?
                # search.py: DataManager.add_loan(user.email, book.isbn, due_date)
                # It does NOT store title.
                # So we can't display title unless we fetch it.
                # Ideally DataManager.add_loan should store title too.
                # For now let's say "Book (ISBN)"
                
                due_date = datetime.strptime(record['due_date'], "%Y-%m-%d")
                time_left = due_date - now
                
                if timedelta(seconds=0) < time_left <= timedelta(hours=24):
                    alerts.append(f"Reminder: Book ({record['isbn']}) is due in less than 24 hours.")
                elif time_left.total_seconds() < 0:
                    alerts.append(f"Overdue: Book ({record['isbn']}) was due on {due_date.strftime('%Y-%m-%d')}.")
            except:
                pass
                
        return alerts

    def get_history(self):
        from utils.data_manager import DataManager
        return DataManager.get_user_history(self.email)
