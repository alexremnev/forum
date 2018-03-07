import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.Permission import Permission
from app.business import encrypt_password, verify_password, permission_required, admin_required, is_unique_post_title
from app.forms import RegisterForm, LoginForm, PostForm, CommentForm
from app.models import User, Post, Comment, Role


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    search = request.args.get('search')
    query = Post.query
    if search is not None and len(search) > 2:
        query = query.filter(Post.title.like("%{0}%".format(search)))
    posts = query.all()
    if len(posts) < 1:
        return render_template('posts.html', msg='Not Found')
    return render_template('posts.html', posts=posts, Permission=Permission)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
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
@login_required
def edit_post(id):
    if [post.id for post in current_user.posts if str(post.id) == id] or current_user.can(Permission.MODERATE_COMMENTS):
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
@permission_required(Permission.MODERATE_COMMENTS)
def delete_post(id):
    db.session.query(Post).filter_by(id=id).delete()
    db.session.commit()
    flash('Post Removed', 'success')
    return redirect(url_for('posts'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_role = Role.query.filter_by(name='user').first()
        new_user = User(username=form.username.data, email=form.email.data,
                        password=(encrypt_password(form.password.data)), role=user_role)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
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
            if verify_password(form.password.data, user.password):
                login_user(user, remember=form.remember.data)
                flash('You were successfully logged in', 'success')
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
        else:
            error = 'Invalid username or password'
    return render_template('login.html', form=form, error=error)


@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin.html', users=users, roles=roles)


@app.route('/assign/<string:id>/', methods=['GET', 'POST'])
@admin_required
def assign(id):
    role_id = request.form.get('assign')
    db.session.query(User).filter_by(id=id).update({'role_id': role_id})
    db.session.commit()
    flash('Role added', 'success')
    return redirect(url_for('admin'))


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template('user.html', user=user, posts=posts)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))
