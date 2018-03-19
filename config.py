import os

DEBUG = True

WTF_CSRF_ENABLED = True

SECRET_KEY = "secretKey"

SQLALCHEMY_TRACK_MODIFICATIONS = False

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'forum.db')

PAGE_SIZE = 5