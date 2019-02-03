import sys
import os
import platform
import json
from pathlib import Path, PureWindowsPath
from loguru import logger
import itertools
import pandas as pd

import pprint

from config_vars import (
    ats_dir,
    warn,
    ats_dir_win,
    jcl_dir,
    json_dir,
    strategy_code_dir,
    jcl_code_dir,
    strategy_code_dir,
    rpt_dir,
)

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
from data_prep_tools import setSessionVars, setDataSeries
from ats_template_tools import formatCommentStrings, setHeader
from db_query import connectDB
from db_query import (
    nextStrategyId,
    queryCandidate,
    queryCandidateSettings,
    queryCandidateParams,
    queryLogic,
    queryParamDef,
    queryStrategy,
    queryStrategySettings,
    queryStrategyParams,
)
from db_insert_update import (
    dbInsertStrategySetting,
    dbUpdateStrategy,
    dbInsertStrategyParams,
    dbInsertStrategyOosPeriod,
    dbInsertStrategyOosSetting,
)
from db_other import (
    clear_strategy_settings,
    clear_strategy_parameters,
    clear_strategy_oos_periods,
    clear_strategy_oos_settings,
)
from ats_file_tools import oldest_dp_file_pair, archive_file
from ats_template_tools import parseInput, lsbLogic, poiLogic, filterLogic
from ats_template_tools import timeSegmentLogic, stopLossLogic, profitTargetLogic
from ats_template_tools import processStrategyTemplate


def getStrategySetup(dbh, strat_id):
    logger.debug(f"strat_id = {strat_id}")
    strat = queryStrategy(dbh, strat_id)
    settings = queryStrategySettings(dbh, strat_id)
    params = queryStrategyParams(dbh, strat_id)

    setup = {}
    setup["strat_id"] = strat_id
    setup["cand_id"] = strat.cand_id
    setup["strategy_template_v"] = strat.strategy_template_v
    setup["oos_curve_template_v"] = strat.oos_curve_template_v
    setup["jcl_version"] = strat.jcl_version
    setup["symbol"] = strat.symbol
    setup["chart_series"] = strat.chart_series
    setup["reopt_param_names"] = strat.reopt_param_names
    setup["fitness_func"] = strat.fitness_function
    setup["max_bars_back"] = strat.max_days_back
    setup["oosPercentLast"] = 0
    setup["session_num"] = strat.market_session_id
    setup["session_name"] = f"session {strat.market_session_id}"
    setup["strategy_file"] = strat.strategy_file
    setup["strategy_oos_file"] = strat.strategy_oos_file

    setup["sess_start"], setup["sess_end"] = setSessionVars(dbh, setup["session_num"])
    setup["data_series"] = setDataSeries(setup["chart_series"])

    setup["vars"] = {}
    setup["counts"] = {}
    setup["counts"]["el_vars"] = 0
    setup["counts"]["el_inputs"] = 0
    setup["counts"]["data_series"] = 0

    setup["opt_inputs"] = {}
    for p in params:
        logger.debug(f"params:  p={p.name}")
        param_name, param_setup = parseInput(p)
        setup["opt_inputs"][param_name] = param_setup
        setup["vars"][param_name] = param_setup

    setup["param_vars"] = {}
    for s in settings:
        logger.debug(f"settings:  s={s.name}")
        setup["vars"].setdefault(s.name, {})["d_type"] = s.data_type
        setup["vars"][s.name]["setting"] = s.value

    for k in setup["vars"]:
        logger.debug(f"vars:  k={k}")
        if "value" in setup["vars"][k].keys() and isinstance(
            setup["vars"][k]["value"], (list,)
        ):
            setup["vars"][k]["el_block"] = "input"
            setup["counts"]["el_inputs"] += 1
        else:
            setup["vars"][k]["el_block"] = "variable"
            setup["counts"]["el_vars"] += 1

    setup["var_names"] = []
    setup["input_names"] = []
    for k, v in setup["vars"].items():
        logger.debug(f"items:  {v}")
        pprint.pprint(f"*getCandidateSetup: items:  {v}")
        if v["el_block"] == "input":
            setup["input_names"].append(k)
        elif v["el_block"] == "variable":
            setup["var_names"].append(k)
        else:
            warn(f"el_block not defined, strat_id={setup['strat_id']}, var={k}")

    setup["timeframes"] = []
    for ds in setup["chart_series"].split(","):
        i, symbol, tf, unit = ds.split(":")
        tf_d = {"ds": i, "symbol": symbol, "tf": tf, "unit": unit}
        setup["timeframes"].append(tf_d)
        setup["counts"]["data_series"] += 1

    dir = f"{ats_dir}/Data/StrategyCode/"
    if platform.system() == "Windows":
        dir = str(PureWindowsPath(ats_dir_win / strategy_code_dir))

    setup["strategy_name"] = f"strat_{strat_id}"
    setup["strategy_file"] = f"{dir}/{setup['strategy_name']}"

    dir = f"{ats_dir}/Data/OptimizationApiCode/"
    if platform.system() == "Windows":
        dir = str(PureWindowsPath(ats_dir_win / jcl_code_dir))

    setup["jcl_file"] = f"{dir}{setup['strategy_name']}.jcl"

    return setup


def good_logic(logic):
    if not logic["lsb"] or len(logic["lsb"]) == 0:
        logger.debug(f"lsb :{logic['lsb']}")
        pprint.pprint(f"lsb :{logic['lsb']}")
        # return None
    if not logic["poi"] or len(logic["poi"]) == 0:
        logger.debug(f"poi :{logic['poi']}")
        pprint.pprint(f"poi :{logic['poi']}")
        return None
    if not logic["filters"] or len(logic["filters"]) == 0:
        logger.debug(f"filters :{logic['filters']}")
        pprint.pprint(f"filters :{logic['filters']}")
        return None
    if not logic["tseg"] or len(logic["tseg"]) == 0:
        logger.debug(f"tseg :{logic['tseg']}")
        pprint.pprint(f"tseg :{logic['tseg']}")
        return None
    if not logic["stop_loss"] or len(logic["stop_loss"]) == 0:
        logger.debug(f"stop_loss :{logic['stop_loss']}")
        pprint.pprint(f"stop_loss :{logic['stop_loss']}")
        # return None
    if not logic["profit_target"] or len(logic["profit_target"]) == 0:
        logger.debug(f"profit_target :{logic['profit_target']}")
        pprint.pprint(f"profit_target :{logic['profit_target']}")
        # return None
    return True


def generateStrategyCode(dbh, setup):
    logic = {}
    desc = ""    # formatCommentStrings(setup)
    hdr = ""    # setHeader(setup)

    logic["lsb"] = lsbLogic(setup)
    logic["poi"] = poiLogic(dbh, setup)
    logic["filters"] = filterLogic(dbh, setup)
    logic["tseg"] = timeSegmentLogic(setup)
    logic["stop_loss"] = stopLossLogic(setup)
    logic["profit_target"] = profitTargetLogic(setup)

    setup["logic"] = {}
    setup["logic"]["lsb"] = lsbLogic(setup)
    setup["logic"]["poi"] = poiLogic(dbh, setup)
    setup["logic"]["filters"] = filterLogic(dbh, setup)
    setup["logic"]["tseg"] = timeSegmentLogic(setup)
    setup["logic"]["stop_loss"] = stopLossLogic(setup)
    setup["logic"]["profit_target"] = profitTargetLogic(setup)



    logger.debug(logic)
    pprint.pprint(logic)

    if not good_logic(logic):
        warn("Not Good Logic")
        return None

    logger.debug(setup)
    pprint.pprint(setup)

    hdr = ""
    desc = {}
    desc["chart_setup"] = ""
    desc["prototype_info"] = ""

    strat = processStrategyTemplate(setup["strategy_template_v"], hdr, desc, setup, logic)

    logger.debug(f"write Strategy to {setup['strategy_file']}")
    open(setup["strategy_file"], "w").write(strat)
    return strat

def parse_oos_report(fn):
    logger.debug(f"parse_oos_report({fn}):")
    header = True
    with open(fn, "r") as text_file:
        for line in itertools.islice(text_file, 3, 14):
            if header:
                labels = line.split()
                labels[1:2] = "start_dt", "end_dt"
                labels.remove("Ratio")
                labels.remove("Avg")
                df = pd.DataFrame(columns=labels)
                list_of_lists = []
                header = False
            else:
                run, start_dt, _, end_dt, days, bars, np, dd, ddp, nt, pp, wl, at, sd, med, pf, rrr, tt, *params = (
                    line.split()
                )
                params = ",".join(params)
                list_of_lists.append(
                    [
                        run,
                        start_dt,
                        end_dt,
                        days,
                        bars,
                        np,
                        dd,
                        ddp,
                        nt,
                        pp,
                        wl,
                        at,
                        sd,
                        med,
                        pf,
                        rrr,
                        tt,
                        params,
                    ]
                )
    df = pd.DataFrame(list_of_lists, columns=labels)
    df.set_index("Run", inplace=True)
    return df


import glob
from dataclasses import dataclass


@dataclass
class Setting:
    period_id: int = ""
    name: str = ""
    value: str = ""
    data_type: str = ""


def get_historical_params(dbh, setup, cand_id, strat_id):
    print(f"{rpt_dir}/*_cand-{cand_id}/*cand-{cand_id}*_OOS*.txt")
    oos_fn = glob.glob(f"{rpt_dir}/*_cand-{cand_id}/*cand-{cand_id}*_OOS*runs.txt")[0]
    df_oos = parse_oos_report(oos_fn)

    var_names = []
    data_types = []
    for rec in setup["reopt_param_names"].split(","):
        n, t = rec.split(":")
        var_names.append(n)
        data_types.append(t)

    setup["oos_curve_params"] = []
    setup["start_dt"] = None
    for i, row in df_oos.iterrows():
        ys, ms, ds = row.start_dt.split("/")
        ye, me, de = row.end_dt.split("/")
        if int(ds) == 0:
            ds = "01"
        if int(de) == 0:
            de = "01"

        start_dt = f"{ms}/{ds}/{ys}"
        end_dt = f"{me}/{de}/{ye}"
        if not setup["start_dt"]:
            setup["start_dt"] = start_dt
        setup["end_dt"] = end_dt
        period_id = dbInsertStrategyOosPeriod(dbh, strat_id, start_dt, end_dt)

        setup["oos_curve_params"].append(f"if Date >= ELDate({ms},{ds},{ys}) and Date < ELDate({me},{de},{ye}) then")
        setup["oos_curve_params"].append(f"begin")

        for i, p in enumerate(row.Parameters.split(",")):
            setup["oos_curve_params"].append(f"    {var_names[i]} = {p};")

            setting = Setting()
            setting.period_id = (period_id,)
            setting.name = (var_names[i],)
            setting.data_type = (data_types[i],)
            setting.value = (p,)
            logger.debug(f"setting: {setting}")
            dbInsertStrategyOosSetting(dbh, strat_id, setting)
        setup["oos_curve_params"].append(f"end;")


def run_update_strategy_settings(dbh, strat_id, cand_id):
    for setting in queryCandidateSettings(dbh, cand_id):
        dbInsertStrategySetting(dbh, strat_id, setting)
    dbUpdateStrategy(dbh, strat_id, {"status": "Strategy", "status_state": "settings"})


def run_update_strategy_reopt_parameters(dbh, strat_id, cand_id):
    reopt_param_names = queryCandidate(dbh, cand_id).reopt_param_names
    dbUpdateStrategy(dbh, strat_id, {"reopt_param_names": reopt_param_names})

    for param in queryCandidateParams(dbh, cand_id):
        dbInsertStrategyParams(dbh, strat_id, param)
    dbUpdateStrategy(
        dbh, strat_id, {"status": "Strategy", "status_state": "reopt_params"}
    )


def run_generate_code(dbh, setup):
    logger.debug(f"processing strategy: {setup['strat_id']}")

    cnt = 0
    cnt += 1
    print("Setup ...")
    pprint.pprint(setup)

    if not generateStrategyCode(dbh, setup):
        logger.debug(
            "could not generate strategy code for strat_id {setup['strat_id']}"
        )
        return None

    dbUpdateStrategy(dbh, setup["strat_id"], {"status": "code", "status_state": "done"})


def run_strategy_setup():
    dbh = connectDB()
    strat_id = nextStrategyId(dbh)
    if not strat_id:
        return None
    cand_id = queryStrategy(dbh, strat_id).cand_id

    clear_strategy_settings(dbh, strat_id)
    clear_strategy_parameters(dbh, strat_id)
    clear_strategy_oos_settings(dbh, strat_id)
    clear_strategy_oos_periods(dbh, strat_id)

    run_update_strategy_settings(dbh, strat_id, cand_id)
    run_update_strategy_reopt_parameters(dbh, strat_id, cand_id)

    setup = getStrategySetup(dbh, strat_id)

    get_historical_params(dbh, setup, cand_id, strat_id)

    with open(f"{json_dir}/strat_{strat_id}.json", "w") as json_file:
        json.dump(setup, json_file)
    run_generate_code(dbh, setup)
