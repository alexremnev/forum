from flask import render_template

from app import app


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