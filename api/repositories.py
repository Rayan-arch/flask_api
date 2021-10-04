from psycopg2 import extras
from db import get_connection


class AuthorsRepository:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)

    def check_exists(self, author_id):
        self.cursor.execute('SELECT id, first_name, last_name FROM authors WHERE id = %s;', (author_id,))

        return self.cursor.fetchone()

    def get_authors(self):
        self.cursor.execute('SELECT id, first_name, last_name FROM authors;')

        return self.cursor.fetchall()

    def add_author(self, *args):
        self.cursor.execute('INSERT INTO authors (first_name, last_name) VALUES (%s,%s) RETURNING id;', args)
        data = self.cursor.fetchone()
        self.connection.commit()

        return data['id']

    def delete_author(self, id):
        self.cursor.execute('DELETE FROM authors WHERE id=%s', (id,))
        self.connection.commit()


class BooksRepository:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)

    def check_exists(self, id):
        self.cursor.execute('SELECT id, title, description FROM books WHERE id=%s;', (id,))
        return self.cursor.fetchone()

    def get_books(self):
        self.cursor.execute('SELECT id, title, author_id, description FROM books;')

        return self.cursor

    def add_one(self, *args):
        self.cursor.execute('INSERT INTO books (title, author_id, description) VALUES (%s,%s,%s) RETURNING id;', args)
        book_id = self.cursor.fetchone()
        self.connection.commit()

        return book_id['id']

    def delete_books(self, book_id):
        self.cursor.execute('DELETE FROM books WHERE id=%s', (book_id,))
        self.connection.commit()


class UsersRepository:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)

    def get_by_username(self, username):
        self.cursor.execute('SELECT user_name, password FROM users WHERE user_name=%s;', (username,))

        return self.cursor.fetchone()

    def save_new(self, username, password):
        self.cursor.execute('INSERT INTO users(user_name,password) VALUES (%s,%s) RETURNING id;', (username, password))
        user_id = self.cursor.fetchone()
        self.connection.commit()

        return user_id['id']
