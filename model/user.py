from sqlalchemy import Column, String
from sqlalchemy_serializer import SerializerMixin
from model import Base


class User(Base, SerializerMixin):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    photo_color = Column(String)
