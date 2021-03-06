import math

from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user

from app.Permission_const import moderator_role_name, admin_role_name
from app.main import bp
from app.auth.utils import permission_required
from app.main.forms import PostForm, CommentForm
from app.services import commentService, postService


@bp.route('/posts')
@permission_required('follow')
def posts():
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    page_size = current_app.config['POST_PER_PAGE']
    posts = postService.list(search=search, page=page, page_size=page_size)
    count = postService.count(search=search)

    pages = math.ceil(count / page_size)
    page_ref = {p: url_for('main.posts', page=p) for p in range(1, pages + 1)}

    if len(posts) < 1:
        return render_template('posts.html', msg='Not Found')
    return render_template('posts.html', posts=posts, page_ref=page_ref, active=page)


@bp.route('/add_post', methods=['GET', 'POST'])
@permission_required('add_post')
def add_post():
    form = PostForm()
    error = None
    if form.validate_on_submit():
        title = form.title.data
        if postService.is_unique_title(title):
            postService.add(title, form.body.data, current_user)
            return redirect(url_for('main.posts'))
        error = 'Title must be unique'
    return render_template('add_post.html', form=form, error=error)


@bp.route('/post/<string:id>/', methods=['GET', 'POST'])
@permission_required('follow')
def post(id):
    form = CommentForm()
    if form.validate_on_submit():
        commentService.add(form.text.data, id, current_user.id)
        flash('Comment Added', 'success')

    post = postService.get(id)
    return render_template('post.html', post=post, form=form, comment_per_page=current_app.config['COMMENT_PER_PAGE'])


@bp.route('/edit_post/<string:id>/', methods=['GET', 'POST'])
@permission_required('edit_post')
def edit_post(id):
    if [p for p in current_user.posts if str(p.id) == id] or (
            current_user.role.name in [admin_role_name, moderator_role_name]):
        form = PostForm()
        if form.validate_on_submit():
            postService.update(id, title=form.title.data, body=form.body.data, user_id=current_user.id)
            flash('Post Updated', 'success')
            return redirect(url_for('main.posts'))
        post = postService.get(id)
        form.title.data = post.title
        form.body.data = post.body
        return render_template('edit_post.html', form=form)
    flash('You don\'t have enough permissions', 'error')
    return redirect(url_for('auth.login'))


@bp.route('/delete_post/<string:id>/', methods=['POST'])
@permission_required('delete_post')
def delete_post(id):
    postService.delete(id)
    flash('Post Removed', 'success')
    return redirect(url_for('main.posts'))
