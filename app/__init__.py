from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from app.models import Anonymous
login.anonymous_user = Anonymous

from app import views, models, errors
