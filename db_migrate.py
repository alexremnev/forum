from app import alembic, create_app

app = create_app()
with app.app_context():
    alembic.revision('added permission table')
    alembic.upgrade()
