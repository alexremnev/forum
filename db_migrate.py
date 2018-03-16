from flask_alembic import Alembic

from app import app

alembic = Alembic()
alembic.init_app(app)

with app.app_context():
    alembic.revision('added permission table')
    alembic.upgrade()
