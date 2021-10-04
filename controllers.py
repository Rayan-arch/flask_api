from hashlib import pbkdf2_hmac
from flask import render_template, request
from api.repositories import UsersRepository
from forms import RegisterForm, LoginForm


def crypt_password(password):
    salt = 'asdfgb244!&%$'
    crypto =  pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        999
    )

    return crypto.hex()

def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        crypted_password = crypt_password(form.password.data)
        repository = UsersRepository()
        data = repository.get_by_username(username)
        print(data['password'])
        print(crypted_password)
        quit()

    return render_template('login.html.jinja2', form=form)


def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = crypt_password(form.password.data)
        repository = UsersRepository()
        repository.save_new(username, password)

    return render_template('register.html.jinja2', form=form)
