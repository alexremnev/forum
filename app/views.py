from flask import render_template, flash, redirect, url_for, request

from app import app
from app.forms import RegisterForm, LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    return render_template('posts.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('You are now registered and can log in', 'success')
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return redirect('/index')
    return render_template('login.html', form=form)
