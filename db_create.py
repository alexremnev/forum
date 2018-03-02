from app import db
from app.models import Role, User
import sys
from passlib.handlers.sha2_crypt import sha256_crypt

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
        admin_roles = Role.query.all()
        admin = User(username=username, email=email, password=sha256_crypt.encrypt(password), roles=admin_roles)
        db.session.add(admin)
        db.session.commit()
    except:
        db.session.rollback()
        print("Invalid args")
        break
