

class Book:
    def __init__(self, isbn, title, author, year, publisher, quantity):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.publisher = publisher
        self.total_quantity = int(quantity)
        self.available_quantity = int(quantity)


    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    @property
    def status(self):
        if self.available_quantity > 0:
            return "Available"
        return "Borrowed" # Simplification, detailed status can be inferred externally using quantity

    def get_info(self):
        return (f"Title: {self.title}\n"
                f"Author: {self.author}\n"
                f"Published: {self.year}\n"
                f"ISBN: {self.isbn}\n"
                f"Available: {self.available_quantity}\n"
                f"Status: {self.status}\n")

    def borrow(self):
        if self.available_quantity > 0:
            self.available_quantity -= 1
            return True
        return False

    def return_book(self):
        if self.available_quantity < self.total_quantity:
            self.available_quantity += 1
