from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user

from app import app
from app.views.utils import permission_required
from app.forms import PostForm, CommentForm
from app.services import commentService, postService


@app.route('/posts')
@permission_required('follow')
def posts():
    search = request.args.get('search')
    all_posts = postService.list(search=search)
    if len(all_posts) < 1:
        return render_template('posts.html', msg='Not Found')
    return render_template('posts.html', posts=all_posts)


@app.route('/add_post', methods=['GET', 'POST'])
@permission_required('add_post')
def add_post():
    form = PostForm()
    error = None
    if form.validate_on_submit():
        title = form.title.data
        if postService.is_unique_post_title(title):
            postService.add(title, form.body.data, current_user)
            return redirect(url_for('posts'))
        error = 'Title must be unique'
    return render_template('add_post.html', form=form, error=error)


@app.route('/post/<string:id>/', methods=['GET', 'POST'])
@permission_required('follow')
def post(id):
    form = CommentForm()
    if form.validate_on_submit():
        commentService.add(form.text.data, id, current_user.id)
        flash('Comment Added', 'success')

    post = postService.get(id)
    return render_template('post.html', post=post, form=form)


@app.route('/edit_post/<string:id>/', methods=['GET', 'POST'])
@permission_required('edit_post')
def edit_post(id):
    if (postService.get_by_user_id(id, current_user.id) is not None) \
            or current_user.role.name in ['admin', 'moderator']:
        form = PostForm()
        if form.validate_on_submit():
            postService.update(id, form.title.data, form.body.data, current_user.id)
            flash('Post Updated', 'success')
            return redirect(url_for('posts'))
        post = postService.get(id)
        form.title.data = post.title
        form.body.data = post.body
        return render_template('edit_post.html', form=form)
    flash('You don\'t have enough permissions', 'error')
    return redirect(url_for('login'))


@app.route('/delete_post/<string:id>/', methods=['POST'])
@permission_required('delete_post')
def delete_post(id):
    postService.delete(id)
    flash('Post Removed', 'success')
    return redirect(url_for('posts'))
