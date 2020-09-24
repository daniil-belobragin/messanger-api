from model.room import Room
from model import db_session

from uuid import uuid1


class RoomService:

    @staticmethod
    def add(room_id, creator_user_id):
        room = Room(room_id, creator_user_id)
        db_session.add(room)
        return room
