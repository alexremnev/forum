from app import db
from app.business import encrypt_password
from app.models import Role, User
import sys
from app.Permission import Permission


def insert_roles():
    roles = {
        'user': (
            Permission.FOLLOW |
            Permission.COMMENT |
            Permission.WRITE_ARTICLE, True),
        'moderator': (
            Permission.FOLLOW |
            Permission.COMMENT |
            Permission.WRITE_ARTICLE |
            Permission.MODERATE_COMMENTS, False),
        'admin': (0xff, False)
    }
    for r in roles:
        role = Role.query.filter_by(name=r).first()
        if role is None:
            role = Role(name=r)
        role.permissions = roles[r][0]
        db.session.add(role)


for arg in [sys.argv]:
    try:
        username = arg[1]
        email = arg[2]
        password = arg[3]
        db.create_all()
        roles = ['user', 'admin', 'moderator']
        for name in roles:
            new_role = Role(name=name)
            db.session.add(new_role)
        insert_roles()
        admin_role = Role.query.filter_by(name='admin').first()
        admin = User(username=username, email=email, password=encrypt_password(password), role=admin_role)
        db.session.add(admin)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        print("Invalid args", exc)
        break
