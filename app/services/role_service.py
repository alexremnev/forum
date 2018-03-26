from app import cache
from app.models.role_permission import Role


class RoleService:

    def __init__(self, session):
        self.session = session

    @cache.cached(100)
    def get_by_name(self, name):
        return self.session.query(Role).filter_by(name=name).first()

    def list(self):
        return self.session.query(Role).all()
