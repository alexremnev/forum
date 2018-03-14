from flask import render_template

from app import app
from app.business import permission_required
from app.models import User, Post


@app.route('/profile/<username>')
@permission_required('profile')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template('user.html', user=user, posts=posts)
