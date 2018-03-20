from functools import wraps

from flask import url_for, redirect, flash
from flask_login import current_user

from app import login
from app.services import userService


def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission_name):
                flash('You don\'t have enough permissions', 'error')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@login.user_loader
def get(id):
    return userService.get(id)
