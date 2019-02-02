import numpy as np
import pandas as pd
import re
import sqlalchemy
import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

import sys

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/Model/v3")

from os import listdir
from pathlib import Path

from base import Base, Session

from session import Session
from prototype import Prototype
from candidate import Candidate
from strategy import Strategy
from market import Market
from dow_optimization import DowOptimization
from oos_test import OosTest


def parseStrategy(fn):
    inputs = []
    vars = []
    logic = []
    oos_params = []
    entry = []
    entry_long = []
    entry_short = []
    stoploss = []
    profittarget = []
    style = []
    other = []
    comment = False

    code_section = ""

    in_fh = open(fn, "r")
    for inline in in_fh:
        s = inline.split("//")[0]
        s = s.strip().rstrip("\n\r").rstrip("\n")
        # s = inline
        # print(s)
        if len(s) < 1:
            continue
        # print(s.upper().strip().replace(' ',''))
        if "INPUTS:" in s.upper():
            code_section = "inputs"
            pattern = re.compile(re.escape("INPUTS:"), re.IGNORECASE)
            s = pattern.sub("", s)
        elif "VARS:" in s.upper():
            code_section = "vars"
            pattern = re.compile(re.escape("VARS:"), re.IGNORECASE)
            s = pattern.sub("", s)
        elif "{" in s:
            comment = True
            #code_section = "comment"
            if "_MARKER_11" in s.upper().strip().replace(" ", ""):
                code_section = "exits"
            elif "_MARKER_4" in s.upper().strip().replace(" ", ""):
                code_section = "logic"
            elif "PLACEOOSCURVEPARAMSHERE" in s.upper().strip().replace(" ", ""):
                code_section = "oos_params"
            if s.endswith("}"):
                comment = False
                #code_section = ""
                s = ""
        elif "IF(MARKETPOSITION=" in s.upper().strip().replace(" ", ""):
            code_section = "entry"
        elif "_MARKER_11" in s.upper().strip().replace(" ", ""):
            code_section = "exits"
        #elif "IFSL_SWITCH=" in s.upper().strip().replace(" ", ""):
        #    code_section = "stoploss"
        #elif "IFPT_SWITCH=" in s.upper().strip().replace(" ", ""):
        #    code_section = "profittarget"
        #elif "IFDAYTRADINGORSWING=" in s.upper().strip().replace(" ", ""):
        #    code_section = "style"

        #if code_section == "comment":
        if comment:
            if "}" in inline:
                pass
                #code_section = ""
        if code_section == "inputs":
            for inp in s.split("//")[0].strip().split(","):
                inp = inp.strip()
                if inp == "":
                    break
                if inp == ";":
                    code_section = ""
                    break
                if inp.endswith(";"):
                    code_section = ""
                    inp = inp.replace(";", "")
                inp = inp.replace("(", "=")
                inp = inp.replace(")", "")
                try:  # myData has no type, and not used
                    dt, tmp = inp.split(" ", 1)
                except:
                    print(f"Exception on {inp}")
                var, val = tmp.strip().split("=")
                inputs.append(f"  {dt} {var}({val})")
        elif code_section == "vars":
            for inp in s.split("//")[0].strip().split(","):
                inp = inp.strip()
                if inp == "":
                    break
                if inp == ";":
                    code_section = ""
                    break
                if inp.endswith(";"):
                    code_section = ""
                    inp = inp.replace(";", "")
                inp = inp.replace("(", "=")
                inp = inp.replace(")", "")
                try:  # myData has no type, and not used
                    dt, tmp = inp.split(" ", 1)
                except:
                    print(f"Exception on {inp}")
                var, val = tmp.strip().split("=")
                vars.append(f"  {dt} {var}({val})")
        elif code_section == "entry":
            if len(s.strip().rstrip("\n")) > 0:
                if "short" in inline.lower():
                    long_short = "short"
                if "long" in inline.lower():
                    long_short = "long"
                entry.append("  " + inline.rstrip("\n"))
                if ";" in inline:
                    if long_short == "long":
                        entry_long = entry
                    if long_short == "short":
                        entry_short = entry
                    entry = []
        elif code_section == "exits":
            #if len(s.strip().rstrip("\n")) > 0:
            exits.append(inline.rstrip("\n"))
        elif code_section == "stoploss":
            if len(s.strip().rstrip("\n")) > 0:
                stoploss.append(inline.rstrip("\n"))
        elif code_section == "profittarget":
            if len(s.strip().rstrip("\n")) > 0:
                profittarget.append(inline.rstrip("\n"))
        elif code_section == "style":
            if len(s.strip().rstrip("\n")) > 0:
                style.append(inline.rstrip("\n"))
        elif code_section == "oos_params":
            oos_params.append(inline.rstrip("\n"))
        elif code_section == "logic":
            logic.append(inline.rstrip("\n"))
        else:
            if len(s.strip().rstrip("\n")) > 0:
                other.append(inline.rstrip("\n"))
        # print(code_section)
    return inputs, vars, logic, oos_params, entry_long, entry_short, stoploss, profittarget, style, exits, other


def modify_strategy_entry(entry_long, entry_short):
    a = []
    a.append("\n".join(entry_long[0:2]))
    a.append("    and dayofweek(date) = DOW")
    a.append("\n".join(entry_long[2:]))

    a.append("\n".join(entry_short[0:2]))
    a.append("    and dayofweek(date) = DOW")
    a.append("\n".join(entry_short[2:]))

    return a


def createDowStrategyFile(strat_file):
    fname = os.path.basename(strat_file)
    dow_dir = (
        "/Users/szagar/ZTS/Dropbox/Business/ats/Data/DOWoptimizations/"
    )
    out_fname = fname.replace(".txt", "_dow_opt.txt")
    out_fname = dow_dir + out_fname
    out_fh = open(out_fname, "w")
    out_fh.write(
        "\n//*********************************\n// Optimization Inputs \n//*********************************\n"
    )
    out_fh.write("Inputs:\n" + ",\n".join(inputs + dow_inputs) + ";")
    out_fh.write(
        "\n//*********************************\n// Variable Definitions \n//*********************************\n"
    )
    out_fh.write("Vars:\n" + ",\n".join(vars + dow_vars) + ";")
    #out_fh.write(
    #    "\n//*********************************\n// Array Definitions \n//*********************************\n"
    #)
    #out_fh.write("Arrays:\n" + ",\n".join(arrs) + ";")
    out_fh.write(
        "\n//*********************************\n// Prep Area \n//*********************************\n"
    )
    out_fh.write("\n".join(dow_prep))

    out_fh.write(
        "\n//*********************************\n// DOW Definitions \n//*********************************\n"
    )
    out_fh.write("\n".join(dow_defs))

    out_fh.write(
        "\n//*********************************\n// OOS Params \n//*********************************\n"
    )
    out_fh.write("\n".join(oos_params))

    out_fh.write(
        "\n//*********************************\n// Strategy Logic \n//*********************************\n"
    )
    out_fh.write("\n".join(logic))
    out_fh.write(
        "\n//*********************************\n// Strategy Entry \n//*********************************\n"
    )
    out_fh.write("\n".join(modify_strategy_entry(entry_long, entry_short)))
    out_fh.write(
        "\n//*********************************\n// MI Premature Exit \n//*********************************\n"
    )
    out_fh.write("\n".join(dow_premature))
    out_fh.write(
        "\n//*********************************\n// Strategy Exit \n//*********************************\n"
    )
    out_fh.write("\n".join(stoploss))
    out_fh.write("\n")
    out_fh.write("\n".join(profittarget))
    out_fh.write("\n")
    out_fh.write("\n".join(exits))
    out_fh.close()

    #print("#################### OTHER ##################")
    #print("\n".join(other))
    #print("#############################################")

    return out_fname


def queryByRobustLevel(level):
    # return session.query(Strategy).filter( Strategy.robust_level == level ).one_or_none()
    # query = session.query(User, Document, DocumentsPermissions).join(Document).join(DocumentsPermissions)
    q = (
        session.query(Strategy, Market)
        .filter(Strategy.robust_level >= level)
        .filter(Strategy.sec_id == Market.id)
        .filter(Strategy.dow_opt == 0)
        .filter(Strategy.status == "oosCurve")
        .filter(Strategy.status_state == "testing")
        .filter(Market.group_1 == "Indices")
        .order_by(Strategy.robust_level)
        .all()
    )
    return q


def queryStrategy(id):
    return session.query(Strategy).filter(Strategy.id == id).one_or_none()


def create_oos_dow_test(dow_file):
    strat_id = str(dow_file).split("_")[1]
    strat = queryStrategy(strat_id)
    new_rec = DowOptimization(
        strat_id=strat.id,
        sec_id=strat.sec_id,
        symbol=strat.symbol,
        dow_file=dow_file,
        oos_start_dt=strat.oos_start_dt,
        oos_end_dt=strat.oos_end_dt,
        dow_switch=1,
        dow_parameter='1,5,1',
        status="new",
        status_state="pending",
    )
    ins = inspect(new_rec)
    session.add(new_rec)
    session.commit()
    return 0


def update_strategy(strat):
    updates = {"dow_opt": strat[0].dow_opt+1}
    try:
        session.query(Strategy).filter(Strategy.id == strat[0].id).update(updates)
        session.commit()
    except:
        session.rollback()
        raise


#################################################################
db = Session()
db_url = os.environ["DB_HEROKU"]

engine = create_engine(db_url)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#mi_template = "/Users/szagar/ZTS/Dropbox/Business/ats/Code/Scripts/addMarketInternals/market_internals.txt"
path = "/Users/szagar/ZTS/Dropbox/Business/ats/Data/OosCurveCode/"

level = 2
for strat in queryByRobustLevel(level):
    print(f"{strat[0].id}: {strat[0].symbol} {strat[0].strategy_oos_file}  level:{strat[0].robust_level}")

    strat_file = Path(
        f"/Users/szagar/ZTS/Dropbox/Business/ats/Data/OosCurveCode/{strat[0].strategy_oos_file}"
    )
    if not strat_file.is_file():
        print(f'*** WARNING :{strat_file} NOT found')
        #continue

    inputs = []
    vars = []
    arrs = []
    logic = []
    oos_params = []
    entry = []
    stoploss = []
    profittarget = []
    style = []
    exits = []
    dow_inputs = []
    dow_vars = []
    dow_prep = []
    dow_defs = []
    dow_premature = []
    print(f"build {strat_file}")
    inputs, vars, logic, oos_params, entry_long, entry_short, stoploss, profittarget, style, exits, other = parseStrategy(
        strat_file
    )
    dow_inputs = ['  int DOW(1)']
    dow_file = createDowStrategyFile(strat_file)
    create_oos_dow_test(os.path.basename(dow_file))
    update_strategy(strat)

