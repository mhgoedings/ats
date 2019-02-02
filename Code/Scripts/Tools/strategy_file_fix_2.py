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


from base import Base,Session

from session import Session
from prototype import Prototype
from candidate import Candidate
from stress_test import StressTest

from strategy import Strategy
from market import Market
from market_internal import MarketInternal

#######################
## Local configuration
#localStrategyDir = '/Users/szagar/ZTS/Dropbox/Business/ats/Data/StrategyArchive/'
localStrategyDir = 'Business/ats/Data/StrategyArchive/'

dbPath = list()
dbPath.append('C:\\ZTS\\Dropbox\\Business\\ats\\Data\\CandidateArchive\\')
dbPath.append('C:\\ZTS\\Dropbox\\Business\\Data\\CandidateArchive\\')
dbPath.append('C:\\ZTS\\Dropbox\\ats\\CandidateArchive\\')

#######################

db = Session()
db_url = os.environ['DB_HEROKU']

engine = create_engine(db_url)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#########################
#strat_query = session.query(Strategy).all()
strat_query = session.query(Strategy).filter(Strategy.status == 'CA', Strategy.status_state == 'done')
#strat_query = session.query(Strategy).filter(Strategy.status == 'CA',
#                                             Strategy.status_state == 'done',
#                                             Strategy.id == 171)


import re

cnt = 0
regex = re.compile(r"_T.*mkt_")

for strat in strat_query:
    cnt += 1
    print(f'{cnt} #({strat.id} proto_id: {strat.proto_id}, cand_id: {strat.cand_id}, strat_id: {strat.id}, symbol: {strat.symbol}')

    print('          ',strat.strategy_file)

    fn = strat.strategy_file
    if fn.startswith('Business/ats/Data/StrategyArchive/strat_'):
      f2 = fn.replace('_DP_','_')
      f2 = regex.sub('_',f2)
    print(f'strat      {f2}')

    oos_file = f2.replace('StrategyArchive','OosCurveCode').replace('.txt','_oos.txt').replace('cand','strat')
    print(f'curvewrote {oos_file}')

    print();

    updates = {'strategy_file': f2, 'strategy_oos_file': oos_file}
    
    try:
      session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
      session.commit()
    except:
      session.rollback()
      raise

session.close()


