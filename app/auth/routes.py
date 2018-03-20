from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user
from werkzeug.urls import url_parse

from app.auth import bp
from app.auth.utils import permission_required
from app.auth.forms import LoginForm, RegisterForm
from app.services import userService


@bp.route('/register', methods=['GET', 'POST'])
@permission_required('register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = userService.add(form.username.data, form.email.data, form.password.data)
        login_user(new_user)
        flash('You are now registered', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
@permission_required('login')
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = userService.get_by_username(form.username.data)
        if user:
            if userService.check_password(form.password.data, user):
                login_user(user, remember=form.remember.data)
                flash('You were successfully logged in', 'success')
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('main.index')
                return redirect(next_page)
        else:
            error = 'Invalid username or password'
    return render_template('auth/login.html', form=form, error=error)


@bp.route('/logout')
@permission_required('logout')
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('auth.login'))
