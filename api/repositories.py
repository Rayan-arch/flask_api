from db import get_connection
from psycopg2 import extras
from auth import User


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

    def map_row_to_user(self, row):
        user = User()
        if row is not None:
            user.id = row['id']
            user.username = row['user_name']
            user.password = row['password']

        else:
            user.id = None
            user.username = None
            user.password = None

        return user

    def get_by_id(self, user_id):
        self.cursor.execute('SELECT id, user_name, password FROM users WHERE id=%s', (user_id))

        return self.map_row_to_user(
            self.cursor.fetchone()
        )


    def get_by_username(self, username):
        self.cursor.execute('SELECT id, user_name, password FROM users WHERE user_name=%s;', (username,))

        return self.map_row_to_user(
            self.cursor.fetchone()
        )

    def save_new(self, username, password):
        self.cursor.execute('INSERT INTO users(user_name,password) VALUES (%s,%s) RETURNING id;', (username, password))
        user_id = self.cursor.fetchone()
        self.connection.commit()

        return user_id['id']
