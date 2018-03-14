import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user

from app import app, db
from app.business import permission_required, is_unique_post_title
from app.forms import PostForm, CommentForm
from app.models import Post, Comment


@app.route('/posts')
def posts():
    search = request.args.get('search')
    query = Post.query
    if search is not None and len(search) > 2:
        query = query.filter(Post.title.like("%{0}%".format(search)))
    posts = query.all()
    if len(posts) < 1:
        return render_template('posts.html', msg='Not Found')
    return render_template('posts.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
@permission_required('add_post')
def add_post():
    form = PostForm()
    error = None
    if form.validate_on_submit():
        title = form.title.data
        if is_unique_post_title(title):
            body = form.body.data
            post = Post(title=title, body=body, author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts'))
        error = 'Title must bu unique'
    return render_template('add_post.html', form=form, error=error)


@app.route('/post/<string:id>/', methods=['GET', 'POST'])
def post(id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, timestamp=datetime.datetime.utcnow(), user_id=current_user.id,
                          post_id=id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment Added', 'success')

    post = Post.query.get(id)
    return render_template('post.html', post=post, form=form)


@app.route('/edit_post/<string:id>/', methods=['GET', 'POST'])
@permission_required('edit_post')
def edit_post(id):
    if (Post.query.filter_by(id=id, user_id=current_user.id).first() is not None) \
            or current_user.role.name in ['admin', 'moderator']:
        form = PostForm()
        post = Post.query.get(id)
        if form.validate_on_submit():
            db.session.query(Post).filter_by(id=id).update(
                {'title': form.title.data, 'body': form.body.data, 'user_id': current_user.id})
            db.session.commit()
            flash('Post Updated', 'success')
            return redirect(url_for('posts'))
        form.title.data = post.title
        form.body.data = post.body
        return render_template('edit_post.html', form=form)
    flash('You don\'t have enough permissions', 'error')
    return redirect(url_for('login'))


@app.route('/delete_post/<string:id>/', methods=['POST'])
@permission_required('delete_post')
def delete_post(id):
    db.session.query(Post).filter_by(id=id).delete()
    db.session.commit()
    flash('Post Removed', 'success')
    return redirect(url_for('posts'))
