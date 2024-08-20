import sqlite3
import json

class Database:
    def __init__(self, db_name='library.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT,
                    year INTEGER,
                    genre TEXT,
                    tags TEXT,
                    description TEXT,
                    download_links TEXT
                );
            ''')

    def execute_query(self, query, params=()):
        with self.conn:
            return self.conn.execute(query, params)

    def fetchall(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

class Book:
    def __init__(self, title, author, year, genre, tags, description, download_links):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.tags = tags
        self.description = description
        self.download_links = json.dumps(download_links)

class Library:
    def __init__(self):
        self.db = Database()

    def add_book(self, book):
        self.db.execute_query('''
            INSERT INTO books (title, author, year, genre, tags, description, download_links)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (book.title, book.author, book.year, book.genre, book.tags, book.description, book.download_links))

    def update_book(self, book_id, book):
        self.db.execute_query('''
            UPDATE books SET title = ?, author = ?, year = ?, genre = ?, tags = ?, description = ?, download_links = ?
            WHERE id = ?
        ''', (book.title, book.author, book.year, book.genre, book.tags, book.description, book.download_links, book_id))

    def delete_books(self, book_id):
        if '-' in book_id:
            start_id, end_id = map(int, book_id.split('-'))
            self.db.execute_query('DELETE FROM books WHERE id BETWEEN ? AND ?', (start_id, end_id))
        else:
            book_id = int(book_id)
            self.db.execute_query('DELETE FROM books WHERE id = ?', (book_id,))


    def search_books(self, title='', author='', year='', genre='', tags='', description=''):
        query = '''
            SELECT * FROM books WHERE
            title LIKE ? AND
            author LIKE ? AND
            year LIKE ? AND
            genre LIKE ? AND
            tags LIKE ? AND
            description LIKE ?
        '''
        params = (f'%{title}%', f'%{author}%', f'%{year}%', f'%{genre}%', f'%{tags}%', f'%{description}%')
        return self.db.fetchall(query, params)

    def get_all_books(self):
        return self.db.fetchall('SELECT * FROM books')

    def get_book_by_id(self, book_id):
        return self.db.fetchall('SELECT * FROM books WHERE id = ?', (book_id,))
