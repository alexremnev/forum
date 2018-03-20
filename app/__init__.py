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
from app.models.user import AnonymousUser

login.anonymous_user = AnonymousUser

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.models import *
from app.views import post, profile, admin, about, index, comment
