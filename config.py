import os


class Config(object):
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secretKey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'forum.db')
    POST_PER_PAGE = 5
    COMMENT_PER_PAGE = 5
    CACHE_TYPE = 'simple'


class ProductionConfig(Config):
    DEBUG = False
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
