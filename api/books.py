from api.repositories import AuthorsRepository, BooksRepository
from pydantic import ValidationError
from flask import Response, request, abort
from json import dumps, loads
from models import Books


def get_all():
    books = BooksRepository()
    data = books.get_books()

    return Response(dumps(data.fetchall()).encode('utf-8'), mimetype='appictation/jsone')


def add_book():
    repository = AuthorsRepository()
    user_data = loads(request.data.decode('utf-8'))
    try:
        book = Books(**user_data)

        if repository.check_exists(book.author_id) is not None:
            books = BooksRepository()
            data = books.add_one(book.title, book.author_id, book.description)

            return Response(dumps({
                "id": data
            }), mimetype='application/json', status=201)
        else:
            return Response(dumps({"error": "Author does not exists."}),mimetype='application/json', status=400)

    except ValidationError as error:
        return Response(
            error.json(),
            mimetype='application/json',
            status=400
        )


def delete_book(book_id):
    books = BooksRepository()
    if books.check_exists(book_id) is None:
        abort(404, 'Book does not exists, or have been already deleted.')

    books.delete_books(book_id)

    return Response(dumps({
        "status": "ok"
    }), mimetype='application/json', status=200)
