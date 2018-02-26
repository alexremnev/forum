from sqlalchemy import Column, Integer, String

from app import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
