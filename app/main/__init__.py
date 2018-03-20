from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main.routes import index, admin, profile, post, comment, about
