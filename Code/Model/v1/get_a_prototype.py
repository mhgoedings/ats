from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from session import Session
from strategy import Strategy
from candidate import Candidate
from prototype import Prototype
from base import Base 
DATABASE_URL="postgres://hiikokjjrwmqpg:ff6d83e0795990ffb048d526caf295eaad7a45476691991f989be513d4e3a6bb@ec2-54-83-60-13.compute-1.amazonaws.com:5432/d617hc9tos6o76"

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
strat = session.query(Strategy).filter(Strategy.id == 1)
print(strat.first().sec_id)

cand = session.query(Candidate).filter(Candidate.id == strat.first().cand_id)
print(cand.first().strategy_name)
 
