from model.user import User
from model import db_session


class UserService:

    @staticmethod
    def add():
        user = User()
        db_session.add(user)
        db_session.commit()
