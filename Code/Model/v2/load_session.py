from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from session import Session
from prototype import Prototype
from candidate import Candidate
from strategy import Strategy
from base import Base
 
DATABASE_URL="postgres://hiikokjjrwmqpg:ff6d83e0795990ffb048d526caf295eaad7a45476691991f989be513d4e3a6bb@ec2-54-83-60-13.compute-1.amazonaws.com:5432/d617hc9tos6o76"

engine = create_engine(DATABASE_URL)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# Insert a Session in the session table
#new_person = Session(id=1,session_start=800,session_end=1300)
#session.add(new_person)
#session.commit()
 
objects = [
    Session(id=1,session_start=800,session_end=1300),
    Session(id=2,session_start=810,session_end=1300),
    Session(id=3,session_start=825,session_end=1325),
    Session(id=4,session_start=830,session_end=1515),
    Session(id=5,session_start=830,session_end=1315),
    Session(id=6,session_start=830,session_end=1305),
    Session(id=7,session_start=900,session_end=1430),
    Session(id=8,session_start=930,session_end=1600),
    Session(id=9,session_start=930,session_end=1615),
    Session(id=10,session_start=820,session_end=1330),
    Session(id=11,session_start=830,session_end=1615),
]
session.bulk_save_objects(objects)
session.commit()
