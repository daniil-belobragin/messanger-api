from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from model import Base


class Participant(Base, SerializerMixin):
    __tablename__ = "participants"

    id = Column(String, primary_key=True)
    room_id = Column(String, ForeignKey("rooms.id"))
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", foreign_keys=[user_id], cascade="delete")
    is_creator = Column(Boolean)

    def __init__(self, p_id, room_id, user_id, is_creator):
        self.id = p_id
        self.room_id = room_id
        self.user_id = user_id
        self.is_creator = is_creator
