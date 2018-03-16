from flask import render_template, flash, redirect, url_for, request

from app import app
from app.services import userService
from app.services import roleService
from app.views.utils import permission_required


@app.route('/admin', methods=['GET', 'POST'])
@permission_required('admin')
def admin():
    users = userService.list()
    roles = roleService.list()
    return render_template('admin.html', users=users, roles=roles)


@app.route('/assign/<string:id>/', methods=['GET', 'POST'])
@permission_required('admin')
def assign(id):
    role_id = request.form.get('assign')
    userService.update_role(id, role_id)
    flash('Role changed', 'success')
    return redirect(url_for('admin'))
