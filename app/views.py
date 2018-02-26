from functools import wraps

from flask import render_template, flash, redirect, url_for, session
from passlib.handlers.sha2_crypt import sha256_crypt

from app import app, db
from app.forms import RegisterForm, LoginForm
from app.models import User


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
    return render_template('posts.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                        password=(sha256_crypt.encrypt(form.password.data)))
        db.session.add(new_user)
        db.session.commit()
        session['logged_in'] = True
        session['']
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
