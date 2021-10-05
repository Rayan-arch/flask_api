from hashlib import pbkdf2_hmac
from flask import render_template, request, abort, redirect
from api.repositories import UsersRepository
from forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required


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
        user = repository.get_by_username(username)

        if user.password == crypted_password:
            login_user(user)
            return redirect('/home')
        else:
            abort(400)


    return render_template('login.html.jinja2', form=form)

def logout():
    logout_user()

    return redirect('/login')

@login_required
def home():
    return render_template('home.html.jinja2')

def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = crypt_password(form.password.data)
        repository = UsersRepository()
        repository.save_new(username, password)
        return redirect('/login')

    return render_template('register.html.jinja2', form=form)
