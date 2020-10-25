from sqlalchemy import Column, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from model import Base


class Message(Base, SerializerMixin):
    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    room_id = Column(String, ForeignKey("rooms.id"))
    owner = Column(String, ForeignKey("users.id"))
    message = Column(String)

    def __init__(self, m_id, room_id, owner, message):
        self.id = m_id
        self.room_id = room_id
        self.owner = owner
        self.message = message
