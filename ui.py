from tabulate import tabulate
from models import Library, Book
import json

class UserInterface:
    def __init__(self):
        self.library = Library()

    def display_books(self, books):
        table = []
        for book in books:
            table.append([book[0], book[1], book[2], book[3], book[4], book[5]])
        print(tabulate(table, headers=["ID", "Title", "Author", "Year", "Genre", "Tags"], tablefmt="grid"))

    def display_book_details(self, book):
        print(f"\n--- Book Details ---")
        print(f"ID: {book[0]}")
        print(f"Title: {book[1]}")
        print(f"Author: {book[2]}")
        print(f"Year: {book[3]}")
        print(f"Genre: {book[4]}")
        print(f"Tags: {book[5]}")
        print(f"Description: {book[6]}")
        
        download_links = json.loads(book[7])
        if download_links:
            print("\nDownload Links:")
            for fmt, url in download_links.items():
                print(f"  {fmt}: {url}")
        else:
            print("No download links available.")

    def input_book_data(self):
        title = input("Enter title: ")
        author = input("Enter author: ")
        year = input("Enter year: ")
        genre = input("Enter genre: ")
        tags = input("Enter tags (comma-separated): ")
        description = input("Enter description: ")
        download_links = self.input_download_links()
        return Book(title, author, year, genre, tags, description, download_links)

    def input_download_links(self):
        links = {}
        while True:
            format = input("Enter format (e.g., EPUB, PDF) or 'done' to finish: ").strip()
            if format.lower() == 'done':
                break
            link = input(f"Enter download link for {format}: ").strip()
            if not format or not link:
                print("Format and link cannot be empty. Please try again.")
                continue
            links[format] = link
        return links

    def main_menu(self):
        while True:
            print("\n--- Main Menu ---")
            print("1. Add book")
            print("2. Update book")
            print("3. Delete book")
            print("4. Search books")
            print("5. Display all books")
            print("6. Exit")

            choice = input("Select an option: ")

            if choice == '1':
                book = self.input_book_data()
                self.library.add_book(book)
                print("Book added successfully!")
            elif choice == '2':
                book_id = int(input("Enter book ID to update: "))
                book = self.input_book_data()
                self.library.update_book(book_id, book)
                print("Book updated successfully!")
            elif choice == '3':
                book_id = input("Enter book ID or range (e.g., '1' or '1-150'): ").strip()
                confirmation = input(f"Are you sure you want to delete book(s) with ID(s) '{book_id}'? (yes/no): ").strip().lower()
                if confirmation == 'yes':
                    self.library.delete_books(book_id)
                    print("Book(s) deleted successfully!")
                else:
                    print("Deletion canceled.")
            elif choice == '4':
                title = input("Enter title to search: ")
                author = input("Enter author to search: ")
                year = input("Enter year to search: ")
                genre = input("Enter genre to search: ")
                tags = input("Enter tags to search: ")
                description = input("Enter description to search: ")
                books = self.library.search_books(title, author, year, genre, tags, description)
                self.display_books(books)
                book_id = input("Enter book ID to view details or 'back' to return to the main menu: ").strip()
                if book_id.lower() == 'back':
                    continue
                try:
                    book = self.library.get_book_by_id(int(book_id))
                    if book:
                        self.display_book_details(book[0])
                    else:
                        print("Book not found.")
                except ValueError:
                    print("Invalid ID format.")
            elif choice == '5':
                books = self.library.get_all_books()
                self.display_books(books)
                book_id = input("Enter book ID to view details or 'back' to return to the main menu: ").strip()
                if book_id.lower() == 'back':
                    continue
                try:
                    book = self.library.get_book_by_id(int(book_id))
                    if book:
                        self.display_book_details(book[0])
                    else:
                        print("Book not found.")
                except ValueError:
                    print("Invalid ID format.")
            elif choice == '6':
                break
            else:
                print("Invalid option, please try again.")
