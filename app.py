from flask import Flask
from api import authors, books
from controllers import register, login

app = Flask(__name__)
# api url
app.add_url_rule('/authors', view_func=authors.index, methods=['GET'])
app.add_url_rule('/authors/add', view_func=authors.add, methods=['POST'])
app.add_url_rule('/authors/<author_id>', view_func=authors.delete, methods=['DELETE'])

app.add_url_rule('/books', view_func=books.get_all, methods=['GET'])
app.add_url_rule('/books/add', view_func=books.add_book, methods=['POST'])
app.add_url_rule('/books/<book_id>', view_func=books.delete_book, methods=['DELETE'])
# controllers
app.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/register', view_func=register, methods=['POST', 'GET'])