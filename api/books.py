from api.repositories import AuthorsRepository, BooksRepository
from json import dumps, loads
from flask import Response, request, abort


def get_all():
    books = BooksRepository()
    data = books.get_books()

    return Response(dumps(data.fetchall()).encode('utf-8'), mimetype='appictation/jsone')


def add_book():
    user_data = loads(request.data.decode('utf-8'))
    if len(user_data) is 3:
        title, author_id, description = user_data.values()
        author = AuthorsRepository()
        if author.check_exists(author_id) is not None:
            book = BooksRepository()
            data = book.add_one(title, author_id, description)

            return Response(dumps({
                "id": data
            }), mimetype='application/json', status=201)

    abort(404, 'Wrong data, please input dictionary with title,author_id,description only.')


def delete_book(book_id):
    books = BooksRepository()
    if books.check_exists(book_id) is None:
        abort(404, 'Book does not exists, or have been already deleted.')

    books.delete_books(book_id)

    return Response(dumps({
        "status": "ok"
    }), mimetype='application/json', status=200)
