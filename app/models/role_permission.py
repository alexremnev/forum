from flask_security import RoleMixin
from sqlalchemy import Column, Integer, String

from app import db

role_permission = db.Table('role_permission',
                           Column('role_id', Integer, db.ForeignKey('role.id')),
                           Column('permission_id', Integer, db.ForeignKey('permission.id')))


class Role(db.Model, RoleMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    permissions = db.relationship('Permission', secondary='role_permission', back_populates='roles')
    users = db.relationship('User', back_populates='role')


class Permission(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    roles = db.relationship('Role', secondary='role_permission', back_populates='permissions')

    def __int__(self, name):
        self.name = name
