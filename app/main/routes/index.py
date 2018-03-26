from flask import render_template

from app import cache
from app.main import bp


@bp.route('/')
@bp.route('/index')
@cache.cached(timeout=600)
def index():
    return render_template('home.html')
