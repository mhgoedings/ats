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
#from stress_test import StressTest
from oos_test import OosTest

from strategy import Strategy
from market import Market
from market_internal import MarketInternal

#######################
## Local configuration
# localStrategyDir = '/Users/szagar/ZTS/Dropbox/Business/ats/Data/StrategyArchive/'
localStrategyDir = "Business/ats/Data/StrategyArchive/"

dbPath = list()
dbPath.append("C:\\ZTS\\Dropbox\\Business\\ats\\Data\\CandidateArchive\\")
dbPath.append("C:\\ZTS\\Dropbox\\Business\\Data\\CandidateArchive\\")
dbPath.append("C:\\ZTS\\Dropbox\\ats\\CandidateArchive\\")
dbPath.append("C:\\ZTS\\Dropbox\\Business\\ats\\Data\\StrategyArchive\\")

#######################

db = Session()
db_url = os.environ["DB_HEROKU"]

engine = create_engine(db_url)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def formatOosBlock(start_dt, end_dt, input_vars, params):
    # print(f'formatOosBlock: {start_dt}, {end_dt}, {input_vars}')
    str = f"if Date > {start_dt} and Date <= {end_dt} then\n"
    for i, v in enumerate(input_vars.split()):
        # print(f'v: {v}  /  {type(v)}')
        n, t = v.split(":")
        str += f"    {n} = {params[i]};\n"
    return str


def reformatStrategyFilename(fn):
    nfn = fn
    print(f'reformatStrategyFilename: fn={fn}')
    for p in dbPath:
        print(f'reformatStrategyFilename: p={p}')
        nfn = nfn.replace(p, localStrategyDir)
    nfn = nfn.replace("cand", "strat")
    nfn = nfn.replace("\\", "/")  # .replace(' ','\ ')
    return nfn


def createOosCurveStrategy(fname):
    out_fn = (
        fname.replace("StrategyArchive", "OosCurveCode")
        .replace(".txt", "_oos.txt")
        .replace("cand", "strat")
    )

    return out_fn


def calcXactCosts(sid):
    mkt_query = session.query(Market).filter(Market.id == sid).one_or_none()

    if mkt_query is None:
        return (0, 0, 0, 0)

    comm_entry_dol = float(mkt_query.comm_entry_dol)
    comm_exit_dol = float(mkt_query.comm_exit_dol)
    slippage_entry_dol = float(mkt_query.slippage_entry_tick * mkt_query.value_1_tick)
    slippage_exit_dol = float(mkt_query.slippage_exit_tick * mkt_query.value_1_tick)
    return (comm_entry_dol, comm_exit_dol, slippage_entry_dol, slippage_exit_dol)


def relatedMarkets(sec):
    mkt_query = session.query(Market).filter(Market.ts_symbol == sec).one_or_none()
    group_1 = mkt_query.group_1

    mkt_query = session.query(Market).filter(Market.group_1 == group_1).all()
    symbols = []
    for rec in mkt_query:
        symbols.append(f"{rec.id}::{rec.ts_symbol}")
    return symbols


'''
def createStressTests(
    strat_id,
    sec_id,
    symbol,
    oos_file,
    oos_start_dt,
    oos_end_dt,
    comm_entry_dol,
    comm_exit_dol,
    slippage_entry_dol,
    slippage_exit_dol,
):

    for mkt in relatedMarkets(symbol):
        sid, symbol = mkt.split("::")
        new_rec = StressTest(
            strat_id=strat_id,
            sec_id=sid,
            symbol=symbol,
            oos_file=oos_file,
            oos_start_dt=oos_start_dt,
            oos_end_dt=oos_end_dt,
            comm_entry_dol=comm_entry_dol,
            comm_exit_dol=comm_exit_dol,
            slippage_entry_dol=slippage_entry_dol,
            slippage_exit_dol=slippage_exit_dol,
        )
        session.add(new_rec)
        session.flush()
    return 0
'''


#########################
# strat_query = session.query(Strategy).all()
strat_query = session.query(Strategy).filter(
    Strategy.status == "CA", Strategy.status_state == "done"
)
# strat_query = session.query(Strategy).filter(Strategy.status == 'CA',
#                                             Strategy.status_state == 'done',
#                                             Strategy.id == 171)

cnt = 0
for strat in strat_query:
    cnt += 1
    print(
        f"{cnt} #({strat.id} proto_id: {strat.proto_id}, cand_id: {strat.cand_id}, strat_id: {strat.id}, symbol: {strat.symbol}"
    )

    print("          ", strat.strategy_file)

    fn = reformatStrategyFilename(strat.strategy_file)
    print(f"strat      {fn}")

    oos_file = (
        fn.replace("StrategyArchive", "OosCurveCode")
        .replace(".txt", "_oos.txt")
        .replace("cand", "strat")
    )
    print(f"curvewrote {oos_file}")

    print()

    oos_file = 'tbd'

    updates = {"strategy_file": fn, "strategy_oos_file": oos_file}
    print(updates)
    # strat.strategy_file = fn
    # strat.strategy_oos_file = oos_file
    ##strat.update(updates)
    # session.commit()

    #try:
    #    session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
    #    session.commit()
    #except:
    #    session.rollback()
    #    raise
    ## finally:
    ##  session.close()

session.close()

