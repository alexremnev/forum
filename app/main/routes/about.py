from flask import render_template

from app import cache
from app.main import bp


@bp.route('/about')
@cache.cached(timeout=600)
def about():
    return render_template('about.html')
