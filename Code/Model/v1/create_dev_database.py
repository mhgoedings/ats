from base import Base
from sqlalchemy import create_engine

from session import Session
from mkt_future import MktFuture
from prototype import Prototype
from candidate import Candidate
from strategy import Strategy
from oos_report import OosReport
from oos_trade import OosTrade

DATABASE_URL="postgres://hiikokjjrwmqpg:ff6d83e0795990ffb048d526caf295eaad7a45476691991f989be513d4e3a6bb@ec2-54-83-60-13.compute-1.amazonaws.com:5432/d617hc9tos6o76"


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# populate with data 
