from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from session import Session
from prototype import Prototype
from base import Base
 
DATABASE_URL="postgres://hiikokjjrwmqpg:ff6d83e0795990ffb048d526caf295eaad7a45476691991f989be513d4e3a6bb@ec2-54-83-60-13.compute-1.amazonaws.com:5432/d617hc9tos6o76"

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
new_prototype = Prototype(id=100,template='')

'''
new_prototype = Prototype(id=55,template="DP_1TF_120m_sess9",
                          data_set=1,
                          data_block=8,
                          status="CandGen",
                          status_state="Done",
                          cand_prefix="DP_55_@RTY.D_120_na",
                          symbol="@RTY.D",
                          timeframe_1=120,
                          timeframe_1_unit="min",
                          fitness_function="TSI",
                          max_days_back=200,
                          session_id=9,
                          prestart_dt="12/28/14",
                          start_dt="12/30/14",
                          end_dt="12/30/15",
                          use_second_data=FALSE,
                          trades_per_day=1,
                          day_swing=0,
                          sl_switch=0,
                          pt_switch=0,
                )
'''
session.add(new_prototype)
session.commit()
 
