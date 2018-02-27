from flask_security import UserMixin
from sqlalchemy import Column, Integer, String, DateTime

from app import db


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(100))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

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
