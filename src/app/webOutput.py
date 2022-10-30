from flask import render_template
from adminConfig import PAIRS, LIMIT
from . import app
from .apiGateway import api
from .dataProcessor import get_json_report


@app.route('/', methods=['GET'])
def report_page():
    result = render_template('main.html')
    response = app.response_class(result, mimetype='text/html')
    return response


@app.route('/api/rates:2000', methods=['GET'])
def get_rates():
    data = get_json_report(PAIRS, LIMIT, api)
    response = app.response_class(data, mimetype='application/json')
    return response
