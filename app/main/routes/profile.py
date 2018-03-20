from flask import render_template

from app.main import bp
from app.auth.utils import permission_required
from app.models.user import User
from app.models.post import Post


@bp.route('/profile/<username>')
@permission_required('profile')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template('user.html', user=user, posts=posts)
