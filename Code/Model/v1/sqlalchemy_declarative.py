import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    session_start = Column(Integer)
    session_end = Column(Integer)

class Prototype(Base):
    __tablename__ = 'prototype'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    template = Column(String(250), nullable=False)
    data_set = Column(Integer)
    data_block =Column(Integer) 
    status = Column(String(25)) 
    status_state = Column(String(25)) 
    cand_prefix = Column(String(32))
    symbol =  = Column(String(12))
    timeframe_1 = Column(Integer)
    timeframe_1_unit = Column(String(10))
    timeframe_2 = Column(Integer,nullable=True)
    timeframe_2_unit = Column(String(10),nullable=True)
    fitness_function = Column(String(12))
    max_days_back = Column(Integer)
    session_number = Column(Integer, ForeignKey('session.id'))
    prestart_dt = Column(Date)
    start_dt = Column(Date)
    end_dt = Column(Date)
    use_second_data = Column(Boolena)
    lsb = Column(Integer)
    trades_per_day = Column(Integer)
    day_swing = Column(Integer)
    poi_switch = Column(Integer)
    poi_n1 = Column(Integer)
    atr = Column(Integer)
    fract = Column(Numeric(5,2))
    filter_1_switch = Column(Integer,nullable=True)
    filter_1_n1 = Column(Integer,nullable=True)
    filter_1_n2 = Column(Integer,nullable=True)
    filter_2_switch = Column(Integer,nullable=True)
    filter_2_n1 = Column(Integer,nullable=True)
    filter_2_n2 = Column(Integer,nullable=True)
    t_segment = Column(Integer)
    sl_swith = Column(Integer)
    stop_loss = Column(Numeric(12,5))
    pt_switch = Column(Integer)
    profit_target = Columne(Numeric(12,5))

    start_run = Column(datetime,nullable=True)
    end_run = Column(datetime,nullable=True)

    candidates = relationship("Candidate")

class Candidate(Base):
    __tablename__ = 'candidate'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    prototype_id = Column(Integer, ForeignKey('proto_type.id'))
    #prototype = relationship(Prototype)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
