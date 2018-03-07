from flask_login import AnonymousUserMixin
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, DateTime
from hashlib import md5

from app import db
from app.Permission import Permission


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

    def can(self, permissions):
        b = self.role.permissions
        a = self.role is not None and (self.role.permissions & permissions) == permissions
        return a

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

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


class Role(db.Model, RoleMixin):
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    permissions = Column(Integer)
    users = db.relationship('User', back_populates='role')


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    @staticmethod
    def is_admin():
        return False
