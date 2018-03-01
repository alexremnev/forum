from flask_login import AnonymousUserMixin
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import backref

from app import db


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(100))
    roles = db.relationship('Role', secondary='roles_users',
                            backref=backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_in_roles(self, *roles):
        return set(self.roles) & set(roles)


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


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), db.ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), db.ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.roles = ['anonymous']
        self.username = 'anonymous'

    def is_in_roles(self, *roles):
        return set(self.roles) & set(roles)

    @property
    def is_anonymous(self):
        return True
