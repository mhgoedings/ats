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

dbox='/Users/szagar/ZTS/Dropbox/'

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
from shutil import copy

cnt = 0
haves = 0
nots = 0
regex = re.compile(r"_T.*mkt_")

for strat in strat_query:
    cnt += 1

    fn = dbox + strat.strategy_file
    if not os.path.isfile(fn):
      print(f'Can not find: {fn}')
      copy(fn, 'nots')
      nots += 1
    else:
      copy(fn, 'haves')
      haves += 1
session.close()


print(f'count: {cnt}  haves: {haves}  nots: {nots}')
