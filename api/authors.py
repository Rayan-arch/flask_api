from json import dumps, loads
from flask import Response, request, abort
from api.repositories import AuthorsRepository


def index():
    author = AuthorsRepository()
    data = author.get_authors()

    return Response(dumps(data), mimetype='appictation/json')


def add():
    user_data = loads(request.data.decode('utf-8'))
    if len(user_data) == 2:
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        author = AuthorsRepository()
        data = author.add_author(first_name, last_name)

        return Response(dumps({
            "id": data
        }), mimetype='application/json', status=201)

    abort(404, 'Wrong data, please input dictionary with first & last name only.')


def delete(author_id):
    author = AuthorsRepository()
    if author.check_exists(author_id) is not None:
        author.delete_author(author_id)

        return Response(dumps({
            "status": "ok"
        }), mimetype='application/json', status=200)

    abort(404, 'Author does not exists or have been already deleted.')
