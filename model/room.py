from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from model import Base


class Room(Base, SerializerMixin):
    __tablename__ = "rooms"
    id = Column(String, primary_key=True)
    creator_user_id = Column(String, ForeignKey("users.id"))
    creator = relationship("User", foreign_keys=[creator_user_id], load_on_pending=True)
    participants = relationship("Participant", cascade="delete")
    messages = relationship("Message", cascade="delete")

    def __init__(self, r_id, creator_user_id):
        self.id = r_id
        self.creator_user_id = creator_user_id
