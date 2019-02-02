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

# from stress_test import StressTest

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


def is_float(str):
    try:
        float(str)
        return True
    except:  # ValueError:
        return False


def calcXactCosts(sid):
    mkt_query = session.query(Market).filter(Market.id == sid).one_or_none()

    if mkt_query is None:
        return (0, 0, 0, 0)

    #print(f'{sid:5d} {mkt_query.comm_entry_dol} {mkt_query.comm_exit_dol} {mkt_query.slippage_entry_tick} {mkt_query.slippage_exit_tick} {mkt_query.value_1_tick}')
    comm_entry_dol = (
        float(mkt_query.comm_entry_dol) if is_float(mkt_query.comm_entry_dol) else None
    )
    comm_exit_dol = (
        float(mkt_query.comm_exit_dol) if is_float(mkt_query.comm_exit_dol) else None
    )
    slippage_entry_dol = (
        float(mkt_query.slippage_entry_tick * mkt_query.value_1_tick)
        if is_float(mkt_query.slippage_entry_tick) and is_float(mkt_query.value_1_tick)
        else None
    )
    slippage_exit_dol = (
        float(mkt_query.slippage_exit_tick * mkt_query.value_1_tick)
        if is_float(mkt_query.slippage_exit_tick) and is_float(mkt_query.value_1_tick)
        else None
    )
    #print(
    #    f"{comm_entry_dol}, {comm_exit_dol}, {slippage_entry_dol}, {slippage_exit_dol}"
    #)
    return (comm_entry_dol, comm_exit_dol, slippage_entry_dol, slippage_exit_dol)


#########################
def queryTest():
    return session.query(Strategy).filter(Strategy.id == 116).limit(1).all()


"""
    return (
        session.query(Strategy)
        .filter(Strategy.status == "CA", Strategy.status_state == "done")
        .limit(1)
        .all()
    )
"""


def queryCA():
    return session.query(Strategy).filter(
        Strategy.status == "CA", Strategy.status_state == "done"
    )


def queryByStrategy(id):
    return session.query(Strategy).filter(Strategy.id == 54)


# strat_query = session.query(Strategy).filter(Strategy.status == 'CA', Strategy.status_state == 'done')
# strat_query = session.query(Strategy).filter(Strategy.status == 'CA',
#                                             Strategy.status_state == 'done',
#                                             Strategy.id == 171)
# strat_query = session.query(Strategy).filter(Strategy.id == 54)


########################

strat_query = queryCA()
#strat_query = queryTest()
for strat in strat_query:
    sid = strat.sec_id
    (
        comm_entry_dol,
        comm_exit_dol,
        slippage_entry_dol,
        slippage_exit_dol,
    ) = calcXactCosts(sid)
    cost = comm_entry_dol+comm_exit_dol+slippage_entry_dol+slippage_exit_dol
    print(
        f"{strat.symbol:6s}:  comm_en: {comm_entry_dol:6.2f}, comm_ex: {comm_exit_dol:6.2f}, slip_en: {slippage_entry_dol:6.2f}, slip_ex: {slippage_exit_dol:6.2f}  {cost:6.2f}"
    )
