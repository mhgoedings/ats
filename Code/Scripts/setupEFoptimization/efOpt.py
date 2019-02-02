import numpy as np
import pandas as pd
import sqlalchemy
import os
import re
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/Model/v3")

from os import listdir
from pathlib import Path

from base import Base, Session

from session import Session
from prototype import Prototype
from candidate import Candidate
from strategy import Strategy
from market import Market
from ef_optimization import EfOptimization
from oos_test import OosTest


def parseStrategy(fn):
    code_segment = {}
    code_segment["inputs"] = []
    code_segment["vars"] = []
    code_segment["logic"] = []
    # code_segment["entry"] = []
    code_segment["entry_long"] = []
    code_segment["entry_short"] = []
    code_segment["stoploss"] = []
    code_segment["profittarget"] = []
    code_segment["style"] = []
    code_segment["other"] = []
    code_segment["oos_params"] = []

    comment = False
    code_section = ""
    entry = []

    in_fh = open(fn, "r")
    for inline in in_fh:
        s = inline.split("//")[0]
        s = s.strip().rstrip("\n\r").rstrip("\n")
        s1 = ""

        ##### indentify comment markers
        if "{" in s:
            s, s1 = s.split("{")
        if len(s1) > 0:
            comment = True
            comment_code = s1.upper().strip().replace(" ", "")
            if "_MARKER_11" in comment_code:
                code_section = "exits"
            elif "_MARKER_4" in comment_code:
                code_section = "logic"
            elif "PLACEOOSCURVEPARAMSHERE" in comment_code:
                code_section = "oos_params"
            if s.endswith("}"):
                comment = False

        ##### closing comment
        s_code = s.upper().strip().replace(" ", "")
        if comment and "}" in s_code:
            s1, s = s.split("}")
            s_code = s.upper().strip().replace(" ", "")
            comment = False

        if len(s) < 1:
            continue

        ##### idenify code_section
        if "INPUTS:" in s_code:
            code_section = "inputs"
            pattern = re.compile(re.escape("INPUTS:"), re.IGNORECASE)
            s = pattern.sub("", s)
        elif "VARS:" in s_code:
            code_section = "vars"
            pattern = re.compile(re.escape("VARS:"), re.IGNORECASE)
            s = pattern.sub("", s)
        elif "IF(MARKETPOSITION=" in s_code:
            code_section = "entry"
        elif "IFSL_SWITCH=" in s_code:
            code_section = "stoploss"
        elif "IFPT_SWITCH=" in s_code:
            code_section = "profittarget"
        elif "IFDAYTRADINGORSWING=" in s_code:
            code_section = "style"

        ##### process code sections
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
                code_segment["inputs"].append(f"  {dt} {var}({val})")
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
                code_segment["vars"].append(f"  {dt} {var}({val})")
        elif code_section == "entry":
            if len(s.strip().rstrip("\n")) > 0:
                if "short" in inline.lower():
                    long_short = "short"
                if "long" in inline.lower():
                    long_short = "long"
                entry.append("  " + inline.rstrip("\n"))
                if ";" in inline:
                    if long_short == "long":
                        code_segmant["entry_long"] = entry
                    if long_short == "short":
                        code_segment["entry_short"] = entry
                    entry = []
        elif code_section == "exits":
            # if len(s.strip().rstrip("\n")) > 0:
            code_segment["exits"].append(inline.rstrip("\n"))
        elif code_section == "stoploss":
            if len(s.strip().rstrip("\n")) > 0:
                code_segment["stoploss"].append(inline.rstrip("\n"))
        elif code_section == "profittarget":
            if len(s.strip().rstrip("\n")) > 0:
                code_segment["profittarget"].append(inline.rstrip("\n"))
        elif code_section == "style":
            if len(s.strip().rstrip("\n")) > 0:
                code_segment["style"].append(inline.rstrip("\n"))
        elif code_section == "oos_params":
            code_segment["oos_params"].append(inline.rstrip("\n"))
        elif code_section == "logic":
            code_segment["logic"].append(inline.rstrip("\n"))
        else:
            print(f"Code Section: {code_section} not defined")
            if len(s.strip().rstrip("\n")) > 0:
                code_segment["other"].append(inline.rstrip("\n"))
    # return inputs, vars, logic, oos_params, entry_long, entry_short, stoploss, profittarget, style, exits, other
    return code_segment


def modify_strategy_entry(entry_long, entry_short, add_dow=False):
    a = []
    a.append("\n".join(entry_long[0:2]))
    if add_dow:
        a.append("    and dayofweek(date) = DOW")
    a.append("\n".join(entry_long[2:]))

    a.append("\n".join(entry_short[0:2]))
    if add_dow:
        a.append("    and dayofweek(date) = DOW")
    a.append("\n".join(entry_short[2:]))

    return a


def createStrategyFile(strat_file):
    fname = os.path.basename(strat_file)
    opt_dir = "/Users/szagar/ZTS/Dropbox/Business/ats/Data/OptimizationArchive/"
    out_fname = fname.replace(".txt", "_ef_opt.txt")
    out_fname = opt_dir + out_fname
    out_fh = open(out_fname, "w")
    out_fh.write(
        "\n//*********************************\n// Optimization Inputs \n//*********************************\n"
    )
    out_fh.write("Inputs:\n" + ",\n".join(code_segment["inputs"] + ef_inputs) + ";")
    out_fh.write(
        "\n//*********************************\n// Variable Definitions \n//*********************************\n"
    )
    out_fh.write("Vars:\n" + ",\n".join(code_segment["vars"] + ef_vars) + ";")
    # out_fh.write(
    #    "\n//*********************************\n// Array Definitions \n//*********************************\n"
    # )
    # out_fh.write("Arrays:\n" + ",\n".join(arrs) + ";")
    out_fh.write(
        "\n//*********************************\n// Prep Area \n//*********************************\n"
    )
    out_fh.write("\n".join(ef_prep))

    out_fh.write(
        "\n//*********************************\n// DOW Definitions \n//*********************************\n"
    )
    out_fh.write("\n".join(ef_defs))

    out_fh.write(
        "\n//*********************************\n// OOS Params \n//*********************************\n"
    )
    out_fh.write("\n".join(code_segment["oos_params"]))

    out_fh.write(
        "\n//*********************************\n// Strategy Logic \n//*********************************\n"
    )
    out_fh.write("\n".join(code_segment["logic"]))
    out_fh.write(
        "\n//*********************************\n// Strategy Entry \n//*********************************\n"
    )
    out_fh.write(
        "\n".join(
            modify_strategy_entry(
                code_segment["entry_long"], code_segment["entry_short"]
            )
        )
    )
    out_fh.write(
        "\n//*********************************\n// MI Premature Exit \n//*********************************\n"
    )
    out_fh.write("\n".join(dow_premature))
    out_fh.write(
        "\n//*********************************\n// Strategy Exit \n//*********************************\n"
    )
    out_fh.write("\n".join(code_segment["stoploss"]))
    out_fh.write("\n")
    out_fh.write("\n".join(code_segment["profittarget"]))
    out_fh.write("\n")
    out_fh.write("\n".join(code_segment["exits"]))
    out_fh.close()

    # print("#################### OTHER ##################")
    # print("\n".join(code_segment['other']))
    # print("#############################################")

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


def create_oos_test(opt_file):
    strat_id = str(opt_file).split("_")[1]
    strat = queryStrategy(strat_id)
    new_rec = EfOptimization(
        strat_id=strat.id,
        sec_id=strat.sec_id,
        symbol=strat.symbol,
        opt_file=opt_file,
        oos_start_dt=strat.oos_start_dt,
        oos_end_dt=strat.oos_end_dt,
        # dow_switch=1,
        # dow_parameter="1,5,1",
        status="new",
        status_state="pending",
    )
    ins = inspect(new_rec)
    session.add(new_rec)
    session.commit()
    return 0


def update_strategy(strat):
    updates = {"dow_opt": strat[0].dow_opt + 1}
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

# mi_template = "/Users/szagar/ZTS/Dropbox/Business/ats/Code/Scripts/addMarketInternals/market_internals.txt"
path = "/Users/szagar/ZTS/Dropbox/Business/ats/Data/OosCurveCode/"

level = 2
for strat in queryByRobustLevel(level):
    print(
        f"{strat[0].id}: {strat[0].symbol} {strat[0].strategy_oos_file}  level:{strat[0].robust_level}"
    )

    strat_file = Path(
        f"/Users/szagar/ZTS/Dropbox/Business/ats/Data/OosCurveCode/{strat[0].strategy_oos_file}"
    )
    if not strat_file.is_file():
        print(f"*** WARNING :{strat_file} NOT found")
        # continue

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
    ef_inputs = []
    ef_vars = []
    ef_prep = []
    ef_defs = []
    dow_premature = []
    print(f"build {strat_file}")
    # inputs, vars, logic, oos_params, entry_long, entry_short, stoploss, profittarget, style, exits, other = parseStrategy(
    code_segment = parseStrategy(strat_file)
    if add_dow:
        ef_inputs = ["  int DOW(1)"]
    opt_file = createStrategyFile(strat_file)
    create_oos_test(os.path.basename(opt_file))
    update_strategy(strat)
