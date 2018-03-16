from sqlalchemy import Column, Integer, String

from app import db


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    body = Column(String)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
