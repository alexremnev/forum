from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from app.models.user import AnonymousUser

login.anonymous_user = AnonymousUser

from app import errors
from app.models import *
from app.views import post, profile, admin, about, register, index, comment
