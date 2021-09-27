from psycopg2 import extras
from json import dumps, loads
from flask import Response,request, abort
from db import get_connection


def get_all():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT id, title, author_id, description FROM books;')

    return Response(dumps(cursor.fetchall()).encode('utf-8'), mimetype='appictation/jsone')


def add_book():
    data = loads(request.data.decode('utf-8'))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT id, first_name, last_name FROM authors WHERE id=%s;',(data['author_id'],))
    author = cursor.fetchone()
    if author is None:
        abort(404)
    cursor.execute('INSERT INTO books (title, author_id, description) VALUES (%s,%s,%s) RETURNING id;',
                   (data['title'],
                    data['author_id'],
                    data['description']
                    ))
    book_id = cursor.fetchone()[0]
    connection.commit()

    return Response(dumps({
        "id": book_id
    }), mimetype='application/json', status=201)

def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, description FROM books WHERE id=%s;',(book_id,))
    book = cursor.fetchone()
    if book is None:
        abort(404)

    cursor.execute('DELETE FROM books WHERE id=%s',(book_id,))
    connection.commit()

    return Response(dumps({
        "status": "ok"
    }),mimetype='application/json',status=200)