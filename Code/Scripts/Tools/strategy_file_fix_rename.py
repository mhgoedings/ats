# coding: utf-8

import numpy as np
import pandas as pd
import re
import sqlalchemy
import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/Model/v2")


from base import Base, Session

from session import Session
from prototype import Prototype
from candidate import Candidate

# from stress_test import StressTest
from oos_test import OosTest

from strategy import Strategy
from market import Market
from market_internal import MarketInternal

dbox = '/Users/szagar/ZTS/Dropbox/'

#######################

db = Session()
db_url = os.environ["DB_HEROKU"]

engine = create_engine(db_url)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



#########################
strat_query = session.query(Strategy).all()
# strat_query = session.query(Strategy).filter(
#    Strategy.status == "CA", Strategy.status_state == "done"
# )
# strat_query = session.query(Strategy).filter(Strategy.status == 'CA',
#                                             Strategy.status_state == 'done',
#                                             Strategy.id == 171)
#C:\ZTS\Dropbox\Business\ats\Data\StrategyArchive\cand_DP_54_T1_15_T2_1440_mkt_71.txt

cnt = 0
prefix = 'cand_DP_'
for strat in strat_query:
    strat.strategy_file = strat.strategy_file.replace('\\','/')
    (path, fn) = os.path.split(strat.strategy_file)
    if fn.startswith(prefix):
        fname = f'{dbox}Business/ats/Data/StrategyArchive/{fn}'
        if os.path.isfile(fname):
            refact_name = f's_{strat.id}.txt'
            print(f'os.rename({fname}, {dbox}Business/ats/Data/StrategyArchive/{refact_name})')
            os.rename(fname, f'{dbox}Business/ats/Data/StrategyArchive/{refact_name}')
            updates = {"strategy_file": refact_name, "strategy_oos_file": "tbd"}
            print(f"update {strat.id}: {refact_name}")
            try:
                session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
                session.commit()
            except:
                session.rollback()
                raise
        else:
            print(f"Strategy file: {strat.strategy_file} not found")
            #f2 = f'{dbox}Business/ats/Data/StrategyArchive/strat_{strat.id}.txt'
            refact_name = f"s_{strat.id}.txt"
            f2 = f'{dbox}Business/ats/Data/StrategyArchive/{refact_name}'
            print(f'look for: {f2}')
            if(os.path.isfile(f2)):
              print('FOUND')
              updates = {"strategy_file": refact_name, "strategy_oos_file": "tbd"}
              try:
                 session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
                 session.commit()
              except:
                 session.rollback()
                 raise

session.close()
