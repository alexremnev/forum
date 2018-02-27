from flask_alembic import Alembic

from app import app

alembic = Alembic()
alembic.init_app(app)

with app.app_context():
    # don't tuch import below!!!
    from app import models

    alembic.revision('add timestamp to comment')
    alembic.upgrade()
