from sqlalchemy import Column, String
from sqlalchemy_serializer import SerializerMixin
from model import Base


class User(Base, SerializerMixin):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    icon_color = Column(String)

    def __init__(self, u_id, name, icon_color):
        self.id = u_id
        self.name = name
        self.icon_color = icon_color
