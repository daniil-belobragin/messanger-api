from sqlalchemy import Column, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from model import Base


class Message(Base, SerializerMixin):
    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    room_id = Column(String, ForeignKey("rooms.id"))
    owner = Column(String, ForeignKey("users.id"))
    message = Column(String)
