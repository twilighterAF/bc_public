import os
import json

from flask_login import UserMixin, current_user
from loguru import logger

from . import DATABASE, login_manager


class User(DATABASE.Model, UserMixin):
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    login = DATABASE.Column(DATABASE.String(128), unique=True, nullable=False)
    password = DATABASE.Column(DATABASE.String(256), nullable=False)


class UserFilter:
    """Settings from the sidebar"""
    def __init__(self):
        self.limit = 10
        self.exchanger = 'no_exchanger'
        self.pairs = {1: ('Bitcoin (BTC)', 'Альфа cash-in RUB', ''),
                      2: ('Tether TRC20 (USDT)', 'Альфа cash-in RUB', '')}

    @logger.catch()
    def json_dump_file(self):
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json')
        data = {'limit': self.limit, 'exchanger': self.exchanger, 'pairs': self.pairs}

        with open(os.path.join(filepath, 'user_filters.json'), 'r+', encoding='utf-8') as file:
            file_data = json.load(file)
            file_data[str(current_user)] = data
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, indent=2, ensure_ascii=False)

    @logger.catch()
    def get_json_data(self):
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json')

        with open(os.path.join(filepath, 'user_filters.json'), 'r', encoding='utf-8') as file:
            data = json.load(file)
            key = str(current_user)
            self.limit = data[key]['limit']
            self.exchanger = data[key]['exchanger']
            self.pairs = data[key]['pairs']
            return json.dumps(data)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


USER_FILTER = UserFilter()

