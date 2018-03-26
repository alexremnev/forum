from flask import Flask
from flask_alembic import Alembic
from flask_caching import Cache
from flask_compress import Compress
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
from config import DevelopmentConfig

db = SQLAlchemy()
alembic = Alembic()
login = LoginManager()
cache = Cache()
compress = Compress()
from app.models.user import AnonymousUser

login.anonymous_user = AnonymousUser


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    cache.init_app(app)
    compress.init_app(app)
    db.init_app(app)
    alembic.init_app(app)
    login.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app.models import *
