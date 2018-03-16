from sqlalchemy import Column, Integer, String, DateTime

from app import db


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    post_id = Column(Integer, db.ForeignKey('post.id'))
