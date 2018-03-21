from hashlib import md5

from flask_login import AnonymousUserMixin
from flask_security import UserMixin
from sqlalchemy import Column, Integer, String

from app import db
from app.models.role_permission import Role


class User(db.Model, UserMixin):
    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(100))
    role_id = Column(Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def is_active(self):
        return True

    def has_permission(self, permission_name):
        return [perm for perm in self.role.permissions if perm.name == permission_name]

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class AnonymousUser(AnonymousUserMixin):

    def __init__(self):
        from app.Permission_const import anonymous_role
        self.role = Role.query.filter_by(name=anonymous_role.name).first()

    def has_permission(self, permission_name):
        return [perm for perm in self.role.permissions if perm.name == permission_name]
