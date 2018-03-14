from app import db
from app.business import encrypt_password
from app.models import User, Role, Permission
import sys
from app.Permission import admin_role, role_permission, admin_permissions


def set_admin_permissions():
    admin_role.permissions = [Permission(name=p) for p in admin_permissions]
    db.session.add(admin_role)
    db.session.commit()


def insert_roles_and_permissions():
    all_perm = Permission.query.all()

    for (role, permissions) in role_permission.items():
        role_perm = [p for p in all_perm if p.name in permissions]
        role.permissions = role_perm
        db.session.add(role)


for arg in [sys.argv]:
    try:
        username = arg[1]
        email = arg[2]
        password = arg[3]
        db.create_all()
        set_admin_permissions()
        insert_roles_and_permissions()
        admin_role = Role.query.filter_by(name=admin_role.name).first()
        admin = User(username=username, email=email, password=encrypt_password(password), role=admin_role)
        db.session.add(admin)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        print("Invalid args", exc)
        break
