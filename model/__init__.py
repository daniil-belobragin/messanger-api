from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:qwerty@localhost/messenger')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


def init_db():
    from model.room import Room
    from model.user import User
    from model.participant import Participant
    from model.message import Message

    Base.metadata.create_all(bind=engine)
