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
from market_internal_optimization import MarketInternalOptimization
from oos_test import OosTest


def parseVarDef(s):
    vars = []
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
        dt, tmp = inp.split(" ", 1)
        var, val = tmp.strip().split("=")
        vars.append(f"  {dt} {var}({val})")
    return vars


def parseArrayDef(s):
    global code_section
    arrs = []
    for inp in s.split("//")[0].strip().split(","):
        inp = inp.strip()
        print(f"inp={inp}")
        if inp == "":
            break
        if inp == ";":
            code_section = ""
            break
        if inp.endswith(";"):
            print("here")
            code_section = ""
            inp = inp.replace(";", "")
        print(f">>{inp}<<")
        if inp == "":
            print("break")
            break
        arrs.append(inp)
    return arrs


def parseStrategy(fn):
    inputs = []
    vars = []
    logic = []
    entry = []
    entry_long = []
    entry_short = []
    stoploss = []
    profittarget = []
    style = []

    code_section = ""

    in_fh = open(fn, "r")
    for inline in in_fh:
        s = inline.split("//")[0]
        s = s.strip().rstrip("\n\r").rstrip("\n")
        if len(s) < 1:
            continue
        if "INPUTS:" in s.upper():
            code_section = "inputs"
            pattern = re.compile(re.escape("INPUTS:"), re.IGNORECASE)
            s = pattern.sub("", s)
        elif "VARS:" in s.upper():
            code_section = "vars"
            pattern = re.compile(re.escape("VARS:"), re.IGNORECASE)
            s = pattern.sub("", s)
        elif "{" in s:
            code_section = "comment"
            if s.endswith("}"):
                code_section = ""
                s = ""
        elif "IF(MARKETPOSITION=" in s.upper().strip().replace(" ", ""):
            code_section = "entry"
        elif "IFSL_SWITCH=" in s.upper().strip().replace(" ", ""):
            code_section = "stoploss"
        elif "IFPT_SWITCH=" in s.upper().strip().replace(" ", ""):
            code_section = "profittarget"
        elif "IFDAYTRADINGORSWING=" in s.upper().strip().replace(" ", ""):
            code_section = "style"

        if code_section == "comment":
            if "}" in inline:
                code_section = ""
        elif code_section == "inputs":
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
                # print(inp)
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
        elif code_section == "stoploss":
            if len(s.strip().rstrip("\n")) > 0:
                stoploss.append(inline.rstrip("\n"))
        elif code_section == "profittarget":
            if len(s.strip().rstrip("\n")) > 0:
                profittarget.append(inline.rstrip("\n"))
        elif code_section == "style":
            if len(s.strip().rstrip("\n")) > 0:
                style.append(inline.rstrip("\n"))
        else:
            if len(s.strip().rstrip("\n")) > 0:
                logic.append(inline.rstrip("\n"))
        # print(code_section)
    return inputs, vars, logic, entry_long, entry_short, stoploss, profittarget, style


def parseMIcode(fn):
    inputs = []
    vars = []
    logic = []
    entry = []
    stoploss = []
    mi_prep = []
    mi_defs = []
    mi_premature = []
    mi_exit_reset = []

    code_section = ""
    marker = ""
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
        elif "ARRAYS:" in s.upper():
            code_section = "arrays"
            pattern = re.compile(re.escape("ARRAYS:"), re.IGNORECASE)
            s = pattern.sub("", s)
        elif "{" in s:
            code_section = "comment"
            if "_marker_" in s.lower():
                marker = (
                    s.lower()
                    .replace("{", "")
                    .replace("}", "")
                    .strip()
                    .replace("_marker_", "")
                )
                if marker.endswith("_"):
                    marker = marker[:-1]
            if s.endswith("}"):
                code_section = ""
                s = ""
        elif "IF(MARKETPOSITION=" in s.upper().strip().replace(" ", ""):
            code_section = "entry"
        elif "IFSL_SWITCH=" in s.upper().strip().replace(" ", ""):
            code_section = "stoploss"
        elif "IFPT_SWITCH=" in s.upper().strip().replace(" ", ""):
            code_section = "profittarget"
        elif "IFDAYTRADINGORSWING=" in s.upper().strip().replace(" ", ""):
            code_section = "style"

        if marker == "mi_prep_start":
            code_section = "mi_prep_start"
        elif marker == "mi_definitions":
            code_section = "mi_definitions"
        elif marker == "mi_exit_reset":
            code_section = "mi_exit_reset"
        elif marker == "mi_premature_exit":
            code_section = "mi_premature_exit"
        elif marker == "mi_section_end":
            marker = ""
            code_section = ""

        if code_section == "comment":
            if "}" in inline:
                code_section = ""
        elif code_section == "inputs":
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
                dt, tmp = inp.split(" ", 1)
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
                # print(inp)
                dt, tmp = inp.split(" ", 1)
                var, val = tmp.strip().split("=")
                vars.append(f"  {dt} {var}({val})")
            # vars.append(parseVarDef(s))
        elif code_section == "arrays":
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
                if inp == "":
                    break
                arrs.append(inp)
            # arrs = [y for x in arrs for y in x]
            ##return arrs
            # print('call parseArrayDef')
            # arrs.append(parseArrayDef(s))
            # print(f'code_section={code_section}')
        elif code_section == "entry":
            entry.append(inline.rstrip("\n"))
        elif code_section == "stoploss":
            if len(s.strip().rstrip("\n")) > 0:
                stoploss.append(inline.rstrip("\n"))
        elif code_section == "profittarget":
            if len(s.strip().rstrip("\n")) > 0:
                profittarget.append(inline.rstrip("\n"))
        elif code_section == "style":
            if len(s.strip().rstrip("\n")) > 0:
                style.append(inline.rstrip("\n"))
        elif code_section == "mi_prep_start":
            if len(s.strip().rstrip("\n")) > 0:
                mi_prep.append(inline.rstrip("\n"))
        elif code_section == "mi_definitions":
            if len(s.strip().rstrip("\n")) > 0:
                mi_defs.append(inline.rstrip("\n"))
        elif code_section == "mi_exit_reset":
            if len(s.strip().rstrip("\n")) > 0:
                mi_exit_reset.append(inline.rstrip("\n"))
        elif code_section == "mi_premature_exit":
            if len(s.strip().rstrip("\n")) > 0:
                mi_premature.append(inline.rstrip("\n"))

        else:
            if len(s.strip().rstrip("\n")) > 0:
                logic.append(inline.rstrip("\n"))
        # print(code_section)
    return inputs, vars, mi_defs, mi_prep, mi_premature, mi_exit_reset


def modify_strategy_entry(entry_long, entry_short):
    a = []
    a.append("if entry_exit_both <> 2 then")
    a.append("begin")
    # { here insert the FINAL LONG CONDITION AND ORDER + add syntax "and modeLong" }
    a.append("\n".join(entry_long[0:2]))
    a.append("    and modeLong")
    a.append("\n".join(entry_long[2:]))
    # { here insert the FINAL SHORT CONDITION AND ORDER + add syntax "and modeShort" }
    a.append("\n".join(entry_short[0:2]))
    a.append("    and modeShort")
    a.append("\n".join(entry_short[2:]))
    a.append("end else")  # exits only
    a.append("begin")
    # { here insert the FINAL LONG CONDITION AND ORDER (dont add anything else) }
    a.append("\n".join(entry_long))
    # { here insert the FINAL SHORT CONDITION AND ORDER (dont add anything else) }
    a.append("\n".join(entry_short))
    a.append("end;")
    return a


def createMiStrategyFile(strat_file):
    print("******* createMiStrategyFile")
    fname = os.path.basename(strat_file)
    mi_dir = (
        "/Users/szagar/ZTS/Dropbox/Business/ats/Code/Scripts/setupMIoptimization/Output/"
    )
    out_fname = fname.replace(".txt", "_mi_opt.txt")
    print(f"mi_dir={mi_dir}")
    print(f"out_fname={out_fname}")
    out_fname = mi_dir + out_fname
    print(f"out_fname={out_fname}")
    out_fh = open(out_fname, "w")
    out_fh.write(
        "\n//*********************************\n// Optimization Inputs \n//*********************************\n"
    )
    # out_fh.write("Inputs:\n"+",\n".join(inputs)+",\n".join(mi_inputs)+';')
    out_fh.write("Inputs:\n" + ",\n".join(inputs + mi_inputs) + ";")
    out_fh.write(
        "\n//*********************************\n// Variable Definitions \n//*********************************\n"
    )
    # out_fh.write("Vars:\n"+",\n".join(vars)+",\n".join(mi_vars)+';')
    out_fh.write("Vars:\n" + ",\n".join(vars + mi_vars) + ";")
    out_fh.write(
        "\n//*********************************\n// Array Definitions \n//*********************************\n"
    )
    out_fh.write("Arrays:\n" + ",\n".join(arrs) + ";")
    out_fh.write(
        "\n//*********************************\n// Market Internals Prep Area \n//*********************************\n"
    )
    out_fh.write("\n".join(mi_prep))
    out_fh.write(
        "\n//*********************************\n// Market Internals Definitions \n//*********************************\n"
    )
    out_fh.write("\n".join(mi_defs))
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
    out_fh.write("\n".join(mi_premature))
    out_fh.write(
        "\n//*********************************\n// MI Exit Reset\n//*********************************\n"
    )
    out_fh.write("\n".join(mi_exit_reset))
    out_fh.write(
        "\n//*********************************\n// Strategy Exit \n//*********************************\n"
    )
    out_fh.write("\n".join(stoploss))
    out_fh.write("\n".join(profittarget))
    out_fh.close()
    return out_fname


def queryByRobustLevel(level):
    # return session.query(Strategy).filter( Strategy.robust_level == level ).one_or_none()
    # query = session.query(User, Document, DocumentsPermissions).join(Document).join(DocumentsPermissions)
    q = (
        session.query(Strategy, Market)
        .filter(Strategy.robust_level == level)
        .filter(Strategy.sec_id == Market.id)
        .filter(Strategy.mi_opt == 0)
        .filter(Strategy.status == "CA")
        .filter(Strategy.status_state == "done")
        .filter(Market.group_1 == "Indices")
        .order_by(Strategy.robust_level)
        .all()
    )
    return q


def queryStrategy(id):
    return session.query(Strategy).filter(Strategy.id == id).one_or_none()


def create_oos_mi_test(mi_file):
    print("******** create_oos_mi_test")
    # /Users/szagar/ZTS/Dropbox/Business/ats/Data/OosCurveCode/s_24_oos.txt
    print(f"mi_file={mi_file}")
    strat_id = str(mi_file).split("_")[1]
    print(f"strat_id={strat_id}")
    strat = queryStrategy(strat_id)
    print(f"symbol={strat.symbol}")
    print(f"sec_id={strat.sec_id}")
    print(f"oos_file={strat.strategy_oos_file}")
    print(
        f"Create a Market Internal test for symbol {strat.symbol}, strategy {strat_id}"
    )
    new_rec = MarketInternalOptimization(
        strat_id=strat.id,
        sec_id=strat.sec_id,
        symbol=strat.symbol,
        mi_file=mi_file,
        oos_start_dt=strat.oos_start_dt,
        oos_end_dt=strat.oos_end_dt,
        # comm_entry_dol=strat.comm_entry_dol,
        # comm_exit_dol=strat.comm_exit_dol,
        # slippage_entry_dol=strat.slippage_entry_dol,
        # slippage_exit_dol=strat.slippage_exit_dol,
        status="new",
        status_state="pending",
    )
    ins = inspect(new_rec)
    session.add(new_rec)
    session.commit()
    return 0


def update_strategy(strat):
    updates = {"mi_opt": strat.mi_opt+1}
    try:
        session.query(Strategy).filter(Strategy.id == strat.id).update(updates)
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

mi_template = "/Users/szagar/ZTS/Dropbox/Business/ats/Code/Scripts/addMarketInternals/market_internals.txt"
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
    entry = []
    stoploss = []
    profittarget = []
    style = []
    print(f"build {strat_file}")
    inputs, vars, logic, entry_long, entry_short, stoploss, profittarget, style = parseStrategy(
        strat_file
    )
    mi_inputs, mi_vars, mi_defs, mi_prep, mi_premature, mi_exit_reset = parseMIcode(
        mi_template
    )
    mi_file = createMiStrategyFile(strat_file)
    #mi_file = Path(createMiStrategyFile(strat_file))
    create_oos_mi_test(os.path.basename(mi_file))
    update_strategy(strat)

    break
