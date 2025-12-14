import csv
from book import Book
from utils.trie import Trie

class BooksManager:
    def __init__(self, filename, default_quantity=3):
        self.filename = filename
        self.default_quantity = default_quantity
        self.books = {}
        self.trie = Trie()
        self.load_books()

    def load_books(self):
        try:
            with open(self.filename, "r", encoding="utf-8", errors='replace') as f:
                reader = csv.DictReader(f, delimiter=';', quotechar='"')
                for row in reader:
                    book = Book(
                        isbn=row["ISBN"],
                        title=row["Book-Title"],
                        author=row["Book-Author"],
                        year=row["Year-Of-Publication"],
                        publisher=row["Publisher"],
                        quantity=self.default_quantity
                    )
                    self.books[book.isbn] = book
                    # Index fields in Trie
                    self.trie.insert(book.title, book.isbn)
                    self.trie.insert(book.author, book.isbn)
                    self.trie.insert(book.isbn, book.isbn)
                    self.trie.insert(book.publisher, book.isbn)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading books: {e}")

    def get_book(self, isbn):
        return self.books.get(isbn)

    def list_books(self):
        return list(self.books.values())

    def add_book(self, book):
        self.books[book.isbn] = book
        # Index new book
        self.trie.insert(book.title, book.isbn)
        self.trie.insert(book.author, book.isbn)
        self.trie.insert(book.isbn, book.isbn)
        self.trie.insert(book.publisher, book.isbn)
        self.save_books()

    def save_books(self):
        try:
            with open(self.filename, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher"])
                for book in self.books.values():
                    writer.writerow([book.isbn, book.title, book.author, book.year, book.publisher])
            return True
        except Exception:
            return False

    def search_books(self, keyword):
        keyword = keyword.strip()
        if not keyword:
            return []
        
        # Split into multiple keywords for intersection search
        keywords = keyword.split()
        isbns = self.trie.multi_keyword_search(keywords)
        
        results = []
        for isbn in isbns:
            if isbn in self.books:
                results.append(self.books[isbn])
        
        return results
