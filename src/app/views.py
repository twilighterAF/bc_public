import datetime

from flask import render_template, request, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from loguru import logger

from . import app, login_manager, DATABASE
from .api_gateway import API_BEST_CHANGE
from .controller import get_json_report, get_json_currencies, parse_json_response
from .models import User, USER_FILTER


@app.before_first_request
def init():
    login_manager.login_view = 'login_page'
    DATABASE.create_all()
    # new_user = User(login='', password=generate_password_hash(''))
    # DATABASE.session.add(new_user)
    # DATABASE.session.commit()
    

@app.before_request
def open_api_gateway():
    API_BEST_CHANGE.start_api_loop()
    if request.endpoint == 'api_get_rates':
        API_BEST_CHANGE.set_timestamp(datetime.datetime.today())


@app.route('/', methods=['GET'])
@login_required
def main_page():
    response = app.response_class(render_template('main.html'), mimetype='text/html')
    response.set_cookie('user', str(current_user))
    return response


@app.route('/api/rates', methods=['GET'])
@login_required
def api_get_rates():
    USER_FILTER.get_json_data()
    api = API_BEST_CHANGE.get_api()
    data = get_json_report(api)
    response = app.response_class(data, mimetype='application/json')
    return response


@app.route('/api/currencies', methods=['GET'])
@login_required
def api_get_currencies():
    api = API_BEST_CHANGE.get_api()
    data = get_json_currencies(api)
    response = app.response_class(data, mimetype='application/json')
    return response


@logger.catch()
@app.route('/api/receive/sidebar', methods=['POST'])
@login_required
def api_receive_from_sidebar():
    response = app.response_class(status=405)

    if request.method == 'POST':
        data = request.data
        parse_json_response(data)
        response = app.response_class(status=200)
    return response


@app.route('/api/filters', methods=['GET'])
@login_required
def get_user_filters():
    data = USER_FILTER.get_json_data()
    response = app.response_class(data, mimetype='application/json')
    return response


@logger.catch()
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        auth_user = User.query.filter_by(login=login).first()
        logger.info(f'LOGIN | trying login - {login}')

        if auth_user and check_password_hash(auth_user.password, password):
            login_user(auth_user)
            logger.info(f'LOGGED - {login}')
            return redirect('/')
        else:
            flash('Требуются логин и пароль')
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
@login_required
def logout_page():
    logout_user()
    logger.info('LOGOUT')
    return redirect('/login')
