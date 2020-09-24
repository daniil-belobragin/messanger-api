from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy_serializer import SerializerMixin
from model import Base


class Participant(Base, SerializerMixin):
    __tablename__ = "participants"

    id = Column(String, primary_key=True)
    room_id = Column(String, ForeignKey("rooms.id"))
    user_id = Column(String, ForeignKey("users.id"))
    is_creator = Column(Boolean)



