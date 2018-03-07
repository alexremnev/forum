from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from app.models import AnonymousUser
login.anonymous_user = AnonymousUser

from app import views, models, errors
