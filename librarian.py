from member import Member

class Librarian(Member):
    def __init__(self, user_id, name, age, email, password):
        super().__init__(user_id, name, age, email, password, role="librarian")

    def add_book(self, book_manager, book):
        book_manager.add_book(book)
        return f"Book '{book.title}' added successfully."

    def remove_book(self, book_manager, isbn):
        pass
