# coding: utf-8

import numpy as np
import pandas as pd
import re
import sqlalchemy
import os
import re
from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import inspect

import sys

from pathlib import Path

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/Model/v3")


from base import Base, Session

from session import Session
from prototype import Prototype
from candidate import Candidate


from strategy import Strategy
from market import Market
from market_internal import MarketInternal

from oos_test import OosTest

#######################
## Local configuration

#######################

db = Session()
db_url = os.environ["DB_HEROKU"]

engine = create_engine(db_url)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def fix_strategy_file(strat):
    strat_fname = strat.strategy_file
    strat_fname = strat_fname.replace("Business/ats/Data/StrategyArchive/", "")

    updates = {"strategy_file": strat_fname}
    try:
        session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
        session.commit()
    except:
        session.rollback()
        raise


def queryAll():
    return session.query(Strategy).filter(Strategy.id > 0)


########################

strat_query = queryAll()
for strat in strat_query:
    print(
        f"{strat.symbol}:  proto_id: {strat.proto_id}, cand_id: {strat.cand_id}, strat_id: {strat.id}, symbol: {strat.symbol}"
    )

    fix_strategy_file(strat)

session.close()
