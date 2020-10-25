from sqlalchemy import exists
from uuid import uuid4

from service import Service
from model import db_session
from model.participant import Participant


class ParticipantService(Service):

    @classmethod
    def add(cls, room_id, user_id, is_creator=False):
        participant_id = str(uuid4())
        participant = Participant(participant_id, room_id, user_id, is_creator)
        db_session.add(participant)
        db_session.commit()
        return participant

    @classmethod
    def exist_by_id(cls, t_id):
        return db_session.query(exists().where(Participant.id == t_id)).scalar()

    @classmethod
    def by_id(cls, t_id):
        return db_session.query(Participant).filter(Participant.id == t_id).first()

    @classmethod
    def remove_by_id(cls, t_id):
        participant = db_session.query(Participant).filter(Participant.id == t_id).first()
        db_session.delete(participant)
        db_session.commit()
        return participant

    @classmethod
    def by_room_id(cls, room_id):
        participant_models = db_session.query(Participant).filter(Participant.room_id == room_id).all()

        if participant_models is None:
            return {}

        participants = list()
        for participant_model in participant_models:
            participants.append(participant_model.to_dict())

        return participants

    @classmethod
    def exists_by_user_id(cls, user_id):
        return db_session.query(exists().where(Participant.user_id == user_id)).scalar()

    @classmethod
    def exists_by_user_id_room_id(cls, user_id, room_id):
        return db_session.query(exists().where(Participant.user_id == user_id)
                                .where(Participant.room_id == room_id)).scalar()

    @classmethod
    def is_creator(cls, room_id, user_id):
        return db_session.query(exists().where(Participant.user_id == user_id).where(Participant.room_id == room_id)
                                .where(Participant.is_creator.is_(True))).scalar()

    @classmethod
    def remove_by_user_id(cls, user_id):
        participant = db_session.query(Participant).filter(Participant.user_id == user_id).first()
        db_session.delete(participant)
        db_session.commit()
        return participant
