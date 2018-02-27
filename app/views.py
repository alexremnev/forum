import datetime
from functools import wraps

from flask import render_template, flash, redirect, url_for, session, request
from passlib.handlers.sha2_crypt import sha256_crypt

from app import app, db
from app.forms import RegisterForm, LoginForm, PostForm, CommentForm
from app.models import User, Post, Comment


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
@is_logged_in
def posts():
    search = request.args.get('search')
    if search is not None and len(search) > 2:
        posts = Post.query.filter(Post.title.like("%{0}%".format(search))).all()
    else:
        posts = Post.query.all()
    if len(posts) < 1:
        return render_template('posts.html', msg='Not Found')
    return render_template('posts.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
@is_logged_in
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        user = User.query.get(1)
        post = Post(title=title, body=body, author=user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('add_post.html', form=form)


@app.route('/post/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def post(id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, timestamp=datetime.datetime.utcnow(), user_id=1, post_id=id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment Added', 'success')

    post = Post.query.get(id)
    return render_template('post.html', post=post, form=form)


@app.route('/edit_post/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def edit_post(id):
    form = PostForm()
    post = Post.query.get(id)
    if form.validate_on_submit():
        # todo doesn't work!
        # post.title = form.title.data,
        # post.body = form.body.data,
        db.session.query(Post).filter_by(id=id).update({'title': form.title.data, 'body': form.body.data, 'user_id': 1})
        db.session.commit()
        flash('Post Updated', 'success')
        return redirect(url_for('posts'))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@app.route('/delete_post/<string:id>/', methods=['POST'])
@is_logged_in
def delete_post(id):
    db.session.query(Post).filter_by(id=id).delete()
    db.session.commit()
    flash('Post Removed', 'success')
    return redirect(url_for('posts'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                        password=(sha256_crypt.encrypt(form.password.data)))
        db.session.add(new_user)
        db.session.commit()
        session['logged_in'] = True
        flash('You are now registered', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if sha256_crypt.verify(form.password.data, user.password):
                session['logged_in'] = True
                flash('You were successfully logged in', 'success')
                return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))
