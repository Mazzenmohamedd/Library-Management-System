import csv
import os
from datetime import datetime

class Transaction:
    def __init__(self, user_email, book_isbn, transaction_type):
        self.user_email = user_email
        self.book_isbn = book_isbn
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TransactionManager:
    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["User-Email", "Book-ISBN", "Type", "Date"])

    def log_transaction(self, user_email, book_isbn, transaction_type):
        try:
            with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([user_email, book_isbn, transaction_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            return True
        except Exception:
            return False
