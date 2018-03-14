from flask import render_template, flash, redirect, url_for, request

from app import app, db
from app.business import permission_required
from app.models import User, Role


@app.route('/admin', methods=['GET', 'POST'])
@permission_required('admin')
def admin():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin.html', users=users, roles=roles)


@app.route('/assign/<string:id>/', methods=['GET', 'POST'])
@permission_required('admin')
def assign(id):
    role_id = request.form.get('assign')
    db.session.query(User).filter_by(id=id).update({'role_id': role_id})
    db.session.commit()
    flash('Role added', 'success')
    return redirect(url_for('admin'))
