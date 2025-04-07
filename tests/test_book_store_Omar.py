import unittest
from io import StringIO
from unittest.mock import patch

from src.book_store import Book, BookStore


class TestBook(unittest.TestCase):
    def test_book_initialization(self):
        book = Book("1984", "George Orwell", 15.99, 3)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "George Orwell")
        self.assertEqual(book.price, 15.99)
        self.assertEqual(book.quantity, 3)

    @patch("sys.stdout", new_callable=StringIO)
    def test_book_display(self, mock_stdout):
        book = Book("Dune", "Frank Herbert", 25.0, 10)
        book.display()
        output = mock_stdout.getvalue()
        self.assertIn("Title: Dune", output)
        self.assertIn("Author: Frank Herbert", output)
        self.assertIn("Price: $25.0", output)
        self.assertIn("Quantity: 10", output)


class TestBookStore(unittest.TestCase):
    def setUp(self):
        self.store = BookStore()

    def test_add_book(self):
        book = Book("The Hobbit", "Tolkien", 10.5, 4)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.store.add_book(book)
            self.assertIn("Book 'The Hobbit' added to the store.", fake_out.getvalue())
        self.assertIn(book, self.store.books)

    def test_display_books_empty(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.store.display_books()
            self.assertIn("No books in the store.", fake_out.getvalue())

    def test_display_books_non_empty(self):
        book = Book("Frankenstein", "Mary Shelley", 20.0, 5)
        self.store.add_book(book)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.store.display_books()
            output = fake_out.getvalue()
            self.assertIn("Books available in the store:", output)
            self.assertIn("Frankenstein", output)

    def test_search_book_found(self):
        book1 = Book("Dracula", "Bram Stoker", 12.0, 2)
        book2 = Book("dracula", "Not Bram", 9.0, 1)  # case insensitive test
        self.store.add_book(book1)
        self.store.add_book(book2)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.store.search_book("Dracula")
            output = fake_out.getvalue()
            self.assertIn("Found 2 book(s) with title 'Dracula':", output)

    def test_search_book_not_found(self):
        self.store.add_book(Book("Ulysses", "James Joyce", 18.0, 1))
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.store.search_book("The Iliad")
            self.assertIn("No book found with title 'The Iliad'.", fake_out.getvalue())
