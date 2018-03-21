from app import app, alembic

with app.app_context():
    alembic.revision('added permission table')
    alembic.upgrade()
