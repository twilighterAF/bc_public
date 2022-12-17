import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


app = Flask(__name__)
db_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}/users.db'
DATABASE = SQLAlchemy(app)
login_manager = LoginManager(app)

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'env.env')
load_dotenv(dotenv_path=ENV_PATH)

app.config['DEBUG'] = False
app.config['SECRET_KEY'] = bytes(os.getenv('APP_SECRET_KEY'), 'utf-8')
app.config['CSRF_ENABLED'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

FILEPATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'info.zip')

from . import views, models
