from base import Base
from sqlalchemy import create_engine

from session import Session
from market import Market
from prototype import Prototype
from candidate import Candidate
from candidate_tmp import CandidateTmp
from strategy import Strategy
from market_internal import MarketInternal
from oos_test import OosTest
#from oos_report import OosReport
#from oos_trade import OosTrade

import os
DATABASE_URL=os.getenv('DATABASE_URL')


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# populate with data 
