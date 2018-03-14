from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.business import encrypt_password, verify_password, permission_required
from app.forms import RegisterForm, LoginForm
from app.models import User, Role


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


@app.route('/logout')
@permission_required('logout')
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))
