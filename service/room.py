from sqlalchemy import exists

from model.room import Room
from model import db_session
from service import Service


class RoomService(Service):

    @classmethod
    def add(cls, room_id, creator_user_id):
        room = Room(room_id, creator_user_id)
        db_session.add(room)
        db_session.commit()
        return room

    @classmethod
    def exist_by_id(cls, t_id):
        return db_session.query(exists().where(Room.id == t_id)).scalar()

    @classmethod
    def by_id(cls, t_id):
        return db_session.query(Room).filter(Room.id == t_id).first()

    @classmethod
    def remove_by_id(cls, t_id):
        room = db_session.query(Room).filter(Room.id == t_id).first()
        db_session.delete(room)
        db_session.commit()
        return room
