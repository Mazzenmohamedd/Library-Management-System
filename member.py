class Member:
    def __init__(self, user_id, name, age, email, password, role):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.email = email
        self.password = password
        self.role = role
        self.favorites = []

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.email}"

    def add_to_favorites(self, book):
        from utils.data_manager import DataManager
        if DataManager.add_favorite(self.email, book.isbn):
            return True, f"Added '{book.title}' to favorites."
        else:
            return False, "Book is already in favorites."

    def remove_from_favorites(self, book):
        from utils.data_manager import DataManager
        if DataManager.remove_favorite(self.email, book.isbn):
            return True, f"Removed '{book.title}' from favorites."
        else:
            return False, "Book was not in favorites."

    def get_favorites(self):
        from utils.data_manager import DataManager
        return DataManager.get_user_favorites(self.email)
