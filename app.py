from flask import Flask
from api import authors, books
from flask_login import LoginManager
from controllers import register, login, logout, home
from api.repositories import UsersRepository

app = Flask(__name__)

app.config['SECRET_KEY'] = 'khio87^%%&R&^%&R7i64$UH$^&YgyT^&'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    repository = UsersRepository()
    return repository.get_by_id(user_id)


# api url
app.add_url_rule('/authors', view_func=authors.index, methods=['GET'])
app.add_url_rule('/authors/add', view_func=authors.add, methods=['POST'])
app.add_url_rule('/authors/<author_id>', view_func=authors.delete, methods=['DELETE'])

app.add_url_rule('/books', view_func=books.get_all, methods=['GET'])
app.add_url_rule('/books/add', view_func=books.add_book, methods=['POST'])
app.add_url_rule('/books/<book_id>', view_func=books.delete_book, methods=['DELETE'])
# controllers
app.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=logout, methods=['GET'])
app.add_url_rule('/register', view_func=register, methods=['POST', 'GET'])
app.add_url_rule('/home', view_func=home, methods=['GET'])
