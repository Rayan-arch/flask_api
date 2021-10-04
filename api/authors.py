from models import Authors
from json import dumps, loads
from pydantic import ValidationError
from flask import Response, request, abort
from api.repositories import AuthorsRepository


def index():
    author = AuthorsRepository()
    data = author.get_authors()

    return Response(dumps(data), mimetype='appictation/json')


def add():
    repository = AuthorsRepository()
    user_data = loads(request.data.decode('utf-8'))
    try:
        author = Authors(**user_data)
        data = repository.add_author(author.first_name, author.last_name)

        return Response(dumps({
            "id": data
        }), mimetype='application/json', status=201)

    except ValidationError as error:

        return Response(
            error.json(),
            mimetype='application/json',
            status=400
        )


def delete(author_id):
    author = AuthorsRepository()
    if author.check_exists(author_id) is not None:
        author.delete_author(author_id)

        return Response(dumps({
            "status": "ok"
        }), mimetype='application/json', status=200)

    abort(404, 'Author does not exists or have been already deleted.')
