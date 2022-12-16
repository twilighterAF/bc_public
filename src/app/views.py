from flask import render_template, request, make_response, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required

from adminConfig import PAIRS, LIMIT, FILEPATH
from . import app, login_manager
from .apiGateway import call_api, get_api
from .dataProcessor import get_json_report, get_json_currencies
from .models import UserLogin
from .dataBase import DataBase


db = DataBase('users.db')


@app.before_request
def init():
    login_manager.login_view = 'login'
    db.create()


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, db)


@app.route('/', methods=['GET', 'POST'])
@login_required
def main_page():
    result = render_template('main.html')
    response = app.response_class(result, mimetype='text/html')
    return response


@app.route('/api/rates:2000', methods=['GET'])
@login_required
def get_rates():
    call_api()  # temp
    api = get_api()
    data = get_json_report(PAIRS, LIMIT, FILEPATH, api)
    response = app.response_class(data, mimetype='application/json')
    return response


@app.route('/api/currencies:2000', methods=['GET'])
@login_required
def get_currencies():
    api = get_api()
    data = get_json_currencies(api)
    response = app.response_class(data, mimetype='application/json')
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #user = db.get_user_by_login(request.form['login'])
        user, password = request.form['login'], request.form['password']
        print(user, password)
        if user and password:
            #user_login = UserLogin().create(user)
            #login_user(user_login)
            return redirect('/')
        flash('Неверный логин или пароль', 'error')
    return render_template('login.html', title='Авторизация')


@app.route('/logout', methods=['GET'])
def logout():
    response = redirect('/')
    response.set_cookie('logged', 'no')
    return response
