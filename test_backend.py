import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from book import Book
from utils.trie import Trie
from utils.reservation import ReservationQueue
from BooksManager import BooksManager

def test_trie():
    print("Testing Trie...")
    trie = Trie()
    trie.insert("Harry Potter and the Philosopher's Stone", "ISBN1")
    trie.insert("Harry Potter and the Chamber of Secrets", "ISBN2")
    trie.insert("The Hobbit", "ISBN3")
    
    # Test 1: Search single word
    res = trie.search("Harry")
    assert "ISBN1" in res and "ISBN2" in res
    print("PASS: Search 'Harry'")
    
    # Test 2: Search specific word
    res = trie.search("Stone")
    assert "ISBN1" in res and "ISBN2" not in res
    print("PASS: Search 'Stone'")
    
    # Test 3: Multi-keyword intersection
    res = trie.multi_keyword_search(["Harry", "Secrets"])
    assert "ISBN2" in res and "ISBN1" not in res
    print("PASS: Multi-keyword 'Harry Secrets'")
    
    print("Trie Tests Passed!\n")

def test_reservation():
    print("Testing Reservation...")
    book = Book("ISBN1", "Title", "Author", "2020", "Pub", 1)
    
    # Borrow until unavailable
    assert book.borrow() == True
    assert book.borrow() == False
    assert book.status == "Borrowed"
    print("PASS: Borrow logic")
    
    # Reserve
    book.reservations.add_reservation("user1@example.com")
    book.reservations.add_reservation("user2@example.com")
    assert book.status == "Reserved"
    assert len(book.reservations.queue) == 2
    print("PASS: Reservation added")
    
    # Return book
    book.return_book()
    # Logic note: book became available mostly, but reservation queue still holds users.
    # In my logic, return_book just increments quantity. App logic should handle notifying user.
    assert book.available_quantity == 1
    # Check next user
    next_user = book.reservations.pop_next_user()
    assert next_user == "user1@example.com"
    print("PASS: Next user popped")
    
    print("Reservation Tests Passed!\n")

def test_books_manager():
    print("Testing BooksManager Integration...")
    # Create dummy csv if not exists or use existing? 
    # Better to mock or use small test file. avoiding modifying real data.
    # For now just test if class inits and Trie is populated if we add a book manually
    
    manager = BooksManager("dummy.csv")
    book = Book("999", "Test Driven Development", "Kent Beck", "2002", "Addison", 5)
    manager.add_book(book)
    
    res = manager.search_books("Test Driven")
    found = False
    for b in res:
        if b.isbn == "999":
            found = True
            break
    assert found
    print("PASS: Manager Search")
    
    # Clean up
    if os.path.exists("dummy.csv"):
        os.remove("dummy.csv")
    
    print("BooksManager Tests Passed!\n")

if __name__ == "__main__":
    test_trie()
    test_reservation()
    test_books_manager()
