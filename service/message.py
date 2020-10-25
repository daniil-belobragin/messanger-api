from sqlalchemy import exists
from uuid import uuid4

from model import db_session
from model.message import Message
from service import Service


class MessageService(Service):

    @classmethod
    def add(cls, room_id, owner, message):
        message_id = str(uuid4())
        message = Message(message_id, room_id, owner, message)
        db_session.add(message)
        db_session.commit()
        return message

    @classmethod
    def exist_by_id(cls, t_id):
        return db_session.query(exists().where(Message.id == t_id)).scalar()

    @classmethod
    def by_id(cls, t_id):
        return db_session.query(Message).filter(Message.id == t_id).first()

    @classmethod
    def remove_by_id(cls, t_id):
        message = db_session.query(Message).filter(Message.id == t_id).first()
        db_session.delete(message)
        db_session.commit()
        return message

    @classmethod
    def by_room_id(cls, room_id):
        message_models = db_session.query(Message).filter(Message.room_id == room_id).all()

        if message_models is None:
            return {}

        messages = list()
        for message_model in message_models:
            messages.append(message_model.to_dict())

        return messages
