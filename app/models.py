from flask_login import AnonymousUserMixin
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, DateTime
from hashlib import md5

from app import db


class User(db.Model, UserMixin):
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


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    body = Column(String)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    post_id = Column(Integer, db.ForeignKey('post.id'))


role_permission = db.Table('role_permission',
                           Column('role_id', Integer, db.ForeignKey('role.id')),
                           Column('permission_id', Integer, db.ForeignKey('permission.id')))


class Role(db.Model, RoleMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    permissions = db.relationship('Permission', secondary=role_permission, back_populates='roles')
    users = db.relationship('User', back_populates='role')


class Permission(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    roles = db.relationship('Role', secondary=role_permission, back_populates='permissions')

    def __int__(self, name):
        self.name = name


class AnonymousUser(AnonymousUserMixin):

    def __init__(self):
            from app.Permission import anonymous_role
            self.role = Role.query.filter_by(name=anonymous_role.name).first()

    def has_permission(self, permission_name):
        return [perm for perm in self.role.permissions if perm.name == permission_name]
