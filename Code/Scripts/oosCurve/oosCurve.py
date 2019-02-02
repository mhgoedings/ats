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
sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")

from db_query import connectDB,queryXactCosts,queryCaDone
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


def formatOosBlock(start_dt, end_dt, input_vars, params):
    # print(f'formatOosBlock: {start_dt}, {end_dt}, {input_vars}')
    # str = f'if Date > {start_dt} and Date <= {end_dt} then\n'
    ys, ms, ds = start_dt.split("/")
    ye, me, de = end_dt.split("/")
    if int(ds) == 0:
        ds = "01"
    if int(de) == 0:
        de = "01"
    str = f"if Date > ELDate({ms},{ds},{ys}) and Date <= ELDate({me},{de},{ye}) then\nbegin\n"
    for i, v in enumerate(input_vars.split()):
        # print(f'v: {v}  /  {type(v)}')
        n, t = v.split(":")
        str += f"    {n} = {params[i]};\n"
    str += f"end;\n"
    return str


def createOosCurveStrategy(dbh,strat):
    oos_start_dt, oos_end_dt, oos_params = parseOOSparams(dbh,strat)

    strat_fname = strat.strategy_file

    # temporary fix
    strat_fname = strat_fname.replace("Business/ats/Data/StrategyArchive/","")

    oos_fname = strat_fname.replace(".txt", "_oos.txt")

    dbox = "/Users/szagar/ZTS/Dropbox/Business/ats/Data/"
    strat_dir = dbox + "StrategyArchive/"
    oos_dir = dbox + "OosCurveCode/"

    fname = strat.strategy_file

    print(f"strat file={strat_dir+strat_fname}")
    print(f"  oos file={oos_dir+oos_fname}")

    strat_in = Path(strat_dir + strat_fname)
    print(f'strat_in = {strat_in}')
    if not strat_in.exists():
        return
    in_fh = open(strat_in, "r")
    out_fh = open(oos_dir + oos_fname, "w")
    outline = ""
    oos_block_wrote = False
    for inline in in_fh:
        outline = inline
        if "INPUTS:" in inline.upper():
            print("found: INPUTS")
            outline = "//" + inline
            outline += re.sub("(?i)inputs:", "Vars:", inline)
        if "PLACE OOS CURVE PARAMS HERE" in inline.upper() and not oos_block_wrote:
            print("found: PLACE OOS CURVE PARAMS HERE")
            outline += oos_params
            # out_fh.write(oos_params)
            oos_block_wrote = True
        if "PART I: BREAKOUT LEVEL CALCU" in inline.upper() and not oos_block_wrote:
            print("found: PART I: BREAKOUT LEVEL CALCU")
            outline += oos_params
            # out_fh.write(oos_params)
            oos_block_wrote = True
        out_fh.write(outline)

    in_fh.close()
    out_fh.close()
    updates = {
        "strategy_file": strat_fname,
        "strategy_oos_file": oos_fname,
        "oos_start_dt": oos_start_dt,
        "oos_end_dt": oos_end_dt,
        "status": "oosCurve",
        "status_state": "created",
    }
    dbUpdateStrategy(dbh, strat.id, updates)
'''
    try:
        session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
        session.commit()
    except:
        session.rollback()
        raise
'''


def set_status(dbh,strat, status_state):
    updates = {"status": "oosCurve", "status_state": status_state}
    dbUpdateStrategy(dbh, strat.id, updates):
'''
    try:
        session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
        session.commit()
    except:
        session.rollback()
        raise
'''


def is_float(str):
    try:
        float(str)
        return True
    except:  # ValueError:
        return False


'''
def calcXactCosts(sid):
    print(f"calcXactCosts({sid}) entered")
    mkt_query = session.query(Market).filter(Market.id == sid).one_or_none()

    if mkt_query is None:
        return (0, 0, 0, 0)

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
    print(
        f"{comm_entry_dol}, {comm_exit_dol}, {slippage_entry_dol}, {slippage_exit_dol}"
    )
    return (comm_entry_dol, comm_exit_dol, slippage_entry_dol, slippage_exit_dol)
'''

def relatedMarkets(sec):
    mkt_query = session.query(Market).filter(Market.ts_symbol == sec).one_or_none()
    group_1 = mkt_query.group_1

    mkt_query = (
        session.query(Market)
        .filter(Market.group_1 == group_1, Market.ts_status == "verified")
        .all()
    )
    symbols = []
    for rec in mkt_query:
        if rec.ts_symbol == sec:
            continue
        symbols.append(f"{rec.id}::{rec.ts_symbol}")
    return symbols


def createOosTest(strat):
    print(f"Create a OOS test for symbol {strat.symbol}")
    new_rec = OosTest(
        strat_id=strat.id,
        test_type="OosTest",
        sec_id=strat.sec_id,
        symbol=strat.symbol,
        oos_file=strat.strategy_oos_file,
        oos_start_dt=strat.oos_start_dt,
        oos_end_dt=strat.oos_end_dt,
        comm_entry_dol=strat.comm_entry_dol,
        comm_exit_dol=strat.comm_exit_dol,
        slippage_entry_dol=strat.slippage_entry_dol,
        slippage_exit_dol=strat.slippage_exit_dol,
        status="new",
        status_state="pending",
    )
    session.add(new_rec)
    session.commit()
    return 0


def createStressTests(strat):
    for mkt in relatedMarkets(strat.symbol):
        sid, symbol = mkt.split("::")
        print(f"Create a stress test for symbol {symbol}, strat {strat.id}")
        new_rec = OosTest(
            strat_id=strat.id,
            test_type="GroupStress",
            sec_id=sid,
            symbol=symbol,
            oos_file=strat.strategy_oos_file,
            oos_start_dt=strat.oos_start_dt,
            oos_end_dt=strat.oos_end_dt,
            comm_entry_dol=strat.comm_entry_dol,
            comm_exit_dol=strat.comm_exit_dol,
            slippage_entry_dol=strat.slippage_entry_dol,
            slippage_exit_dol=strat.slippage_exit_dol,
            status="new",
            status_state="pending",
        )
        ins = inspect(new_rec)
        session.add(new_rec)
        session.commit()
        # session.refresh(new_rec)
        # print(new_rec.id)
        # session.flush()
    return 0


def parseOOSparams(dbh,strat):
    oos_start_dt = "2100/01/01"
    oos_end_dt = ""
    oos_params = ""
    for rec in strat.oos_param_history.splitlines():
        fields = rec.split("\t")
        params = fields[0].split()
        try:
            start_dt, _, end_dt = fields[1].split()
        except:
            set_status(dbh,strat, f"error in {strat.id}")
            print(f"Error: strat {strat.id}: {fields[1]}")
            exit()

        # print(formatOosBlock(start_dt,end_dt,strat.input_vars,params))
        oos_params += formatOosBlock(start_dt, end_dt, strat.input_vars, params)

        if start_dt < oos_start_dt:
            oos_start_dt = start_dt
        if end_dt > oos_end_dt:
            oos_end_dt = end_dt

    return (oos_start_dt, oos_end_dt, oos_params)


#########################
def queryTest():
    return (
        session.query(Strategy)
        .filter(Strategy.id == 10)
        .limit(1)
        .all()
    )
'''
    return (
        session.query(Strategy)
        .filter(Strategy.status == "CA", Strategy.status_state == "done", Strategy.robust_level > 1)
        .limit(1)
        .all()
    )
'''


'''
def queryCA():
    return session.query(Strategy).filter(
        Strategy.status == "CA", Strategy.status_state == "done", Strategy.robust_level > 1
    )
'''


def queryByStrategy(id):
    return session.query(Strategy).filter(Strategy.id == 54)


# strat_query = session.query(Strategy).filter(Strategy.status == 'CA', Strategy.status_state == 'done')
# strat_query = session.query(Strategy).filter(Strategy.status == 'CA',
#                                             Strategy.status_state == 'done',
#                                             Strategy.id == 171)
# strat_query = session.query(Strategy).filter(Strategy.id == 54)


def addXactCosts(dbh,strat):
    (
        comm_entry_dol,
        comm_exit_dol,
        slippage_entry_dol,
        slippage_exit_dol,
    ) = queryXactCosts(dbh,sec_id=strat.sec_id)
    #) = calcXactCosts(strat.sec_id)

    updates = {
        "status": "oosCurve",
        "status_state": "xactCosts",
        "comm_entry_dol": comm_entry_dol,
        "comm_exit_dol": comm_exit_dol,
        "slippage_entry_dol": slippage_entry_dol,
        "slippage_exit_dol": slippage_exit_dol,
    }
    pprint(updates)
    dbUpdateStrategy(dbh, strat.id, updates)
'''
    try:
        session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
        session.commit()
    except:
        session.rollback()
        raise
'''

def create_mi_optimization():
    pass

########################

dbh = connectDB()

strat_query = queryCaDone(dbh)
#strat_query = queryTest()
for strat in strat_query:
    print(
        f"{strat.symbol}:  proto_id: {strat.proto_id}, cand_id: {strat.cand_id}, strat_id: {strat.id}, symbol: {strat.symbol}"
    )

    if strat.robust_level == 0:
        pass
    elif strat.robust_level == 1:
        pass
    elif strat.robust_level == 2:
        if strat.mi_opt == 0:
            create_mi_optimization()
        createOosCurveStrategy(dbh,strat)
        addXactCosts(dbh,strat)
        createOosTest(strat)
        createStressTests(strat)
        set_status(dbh,strat, "testing")
    elif strat.robust_level == 3:
        if strat.mi_opt == 0:
            create_mi_optimization()
        createOosCurveStrategy(dbh,strat)
        addXactCosts(dbh,strat)
        createOosTest(strat)
        createStressTests(strat)
        set_status(dbh,strat, "testing")
    else:
        print(f"WARNING: UnKnown Robust Level: {strat.robust_level}")


session.close()


exit()
