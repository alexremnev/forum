from flask import render_template, flash, redirect, url_for, request

from app.main import bp
from app.services import userService, roleService
from app.auth.utils import permission_required


@bp.route('/admin', methods=['GET', 'POST'])
@permission_required('admin')
def admin():
    users = userService.list()
    roles = roleService.list()
    return render_template('admin.html', users=users, roles=roles)


@bp.route('/assign/<string:id>/', methods=['GET', 'POST'])
@permission_required('admin')
def assign(id):
    role_id = request.form.get('assign')
    userService.update_role(id, role_id)
    flash('Role changed', 'success')
    return redirect(url_for('main.admin'))
