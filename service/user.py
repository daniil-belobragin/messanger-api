from uuid import uuid4
from sqlalchemy import exists

from model.user import User
from model import db_session
from service import Service


class UserService(Service):

    @classmethod
    def add(cls, name, icon_color):
        user_id = str(uuid4())
        user = User(user_id, name, icon_color)
        db_session.add(user)
        db_session.commit()
        return user

    @classmethod
    def exist_by_id(cls, t_id):
        return db_session.query(exists().where(User.id == t_id)).scalar()

    @classmethod
    def by_id(cls, t_id):
        return db_session.query(User).filter(User.id == t_id).first()

    @classmethod
    def remove_by_id(cls, t_id):
        user = db_session.query(User).filter(User.id == t_id).first()
        db_session.delete(user)
        db_session.commit()
        return user
