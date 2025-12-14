import json
import os
from datetime import datetime

LOANS_FILE = "loans.json"
RESERVATIONS_FILE = "reservations.json"
HISTORY_FILE = "history.json"
FAVORITES_FILE = "favorites.json"

class DataManager:
    @staticmethod
    def load_json(filename):
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return {}

    @staticmethod
    def save_json(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_loans():
        return DataManager.load_json(LOANS_FILE)

    @staticmethod
    def save_loans(loans_data):
        DataManager.save_json(LOANS_FILE, loans_data)

    @staticmethod
    def add_loan(user_email, book_isbn, due_date_str):
        data = DataManager.load_loans()
        if user_email not in data:
            data[user_email] = []
        
        # Check if already borrowed
        for loan in data[user_email]:
            if loan['isbn'] == book_isbn:
                return False

        data[user_email].append({
            "isbn": book_isbn,
            "due_date": due_date_str,
            "borrowed_date": datetime.now().strftime("%Y-%m-%d")
        })
        DataManager.save_loans(data)
        return True

    @staticmethod
    def remove_loan(user_email, book_isbn):
        data = DataManager.load_loans()
        if user_email in data:
            for i, loan in enumerate(data[user_email]):
                if loan['isbn'] == book_isbn:
                    del data[user_email][i]
                    DataManager.save_loans(data)
                    return True
        return False

    @staticmethod
    def get_user_loans(user_email):
        data = DataManager.load_loans()
        return data.get(user_email, [])

    # --- HISTORY PERSISTENCE ---
    @staticmethod
    def load_history():
        return DataManager.load_json(HISTORY_FILE)

    @staticmethod
    def add_history(user_email, record):
        data = DataManager.load_history()
        if user_email not in data:
            data[user_email] = []
        
        data[user_email].append(record)
        DataManager.save_json(HISTORY_FILE, data)

    @staticmethod
    def get_user_history(user_email):
        data = DataManager.load_history()
        return data.get(user_email, [])

    # --- FAVORITES PERSISTENCE ---
    @staticmethod
    def load_favorites():
        return DataManager.load_json(FAVORITES_FILE)

    @staticmethod
    def save_favorites(data):
        DataManager.save_json(FAVORITES_FILE, data)

    @staticmethod
    def add_favorite(user_email, isbn):
        data = DataManager.load_favorites()
        if user_email not in data:
            data[user_email] = []
        
        if isbn not in data[user_email]:
            data[user_email].append(isbn)
            DataManager.save_favorites(data)
            return True
        return False

    @staticmethod
    def remove_favorite(user_email, isbn):
        data = DataManager.load_favorites()
        if user_email in data and isbn in data[user_email]:
            data[user_email].remove(isbn)
            DataManager.save_favorites(data)
            return True
        return False

    @staticmethod
    def get_user_favorites(user_email):
        data = DataManager.load_favorites()
        return data.get(user_email, [])

    @staticmethod
    def get_book_likes_count(isbn):
        data = DataManager.load_favorites()
        count = 0
        for user_list in data.values():
            if isbn in user_list:
                count += 1
        return count
