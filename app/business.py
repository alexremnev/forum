from functools import wraps

from flask import url_for, redirect, flash
from flask_login import current_user
from passlib.handlers.sha2_crypt import sha256_crypt

from app import login
from app.Permission import Permission
from app.models import User, Post


def encrypt_password(raw_password):
    return sha256_crypt.encrypt(raw_password)


def verify_password(row_password, encrypted_password):
    return sha256_crypt.verify(row_password, encrypted_password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                flash('You don\'t have enough permissions', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


def is_unique_post_title(title):
    post = Post.query.filter_by(title=title).first()
    return not post
