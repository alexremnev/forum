from app.Permission_const import user_role_name
from app.models.user import User
from app.services.crypto_service import CryptoEngine
from app.services.utils import commit_required


class UserService:

    def __init__(self, session, role_service):
        self.session = session
        self.roleService = role_service

    def get(self, id):
        return self.session.query(User).get(int(id))

    def get_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()

    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    def list(self):
        return self.session.query(User).all()

    def add(self, username, email, password):
        user_role = self.roleService.get_by_name(user_role_name)
        encrypted_password = CryptoEngine.encrypt_password(password)
        new_user = User(username, email, encrypted_password, user_role)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    @commit_required
    def update_role(self, user_id, **kwargs):
        self.session.query(User).filter_by(id=user_id).update(kwargs)

    @staticmethod
    def check_password(password, user):
        return CryptoEngine.verify_password(password, user.password)
