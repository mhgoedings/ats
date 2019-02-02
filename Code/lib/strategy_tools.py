import sys
import os
import platform
import json
from pathlib import Path, PureWindowsPath
from loguru import logger
import itertools

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


import pandas as pd

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
from data_prep_tools import setSessionVars, setDataSeries
from ats_template_tools import formatCommentStrings, setHeader
from db_query import connectDB, queryPrototype, queryCosts, queryPrototypeParams
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
    dbUpdateCandidate,
    dbInsertStrategySetting,
    dbUpdateStrategy,
    dbInsertStrategyParams,
)
from db_other import  (
    clear_strategy_settings,
    clear_strategy_parameters,
)
from ats_file_tools import oldest_dp_file_pair, archive_file
from ats_tools import add_candidate
from ats_template_tools import parseInput, lsbLogic, poiLogic, filterLogic
from ats_template_tools import timeSegmentLogic, stopLossLogic, profitTargetLogic
from ats_template_tools import processStrategyTemplate, processJclTemplate

_param_hash = {}

F1 = 2
F2 = 4
F3 = 8
F4 = 16
F5 = 32
F6 = 64
F7 = 128
F8 = 256
F9 = 512
F10 = 1024
Fmap = {
    F1: "F1",
    F2: "F2",
    F3: "F3",
    F4: "F4",
    F5: "F5",
    F6: "F6",
    F7: "F7",
    F8: "F8",
    F9: "F9",
    F10: "F10",
}


def getStrategySetup(dbh, strat_id):
    logger.debug(f"strat_id = {strat_id}")
    strat = queryStrategy(dbh, strat_id)
    # proto = queryPrototype(dbh, strat.proto_id)
    settings = queryStrategySettings(dbh, strat_id)
    params = queryStrategyParams(dbh, strat_id)

    setup = {}
    # setup["proto_id"]           = proto.id
    setup["strat_id"]             = strat_id
    setup["cand_id"]              = strat.cand_id
    setup["strategy_template_v"]  = strat.strategy_template_v
    setup["oos_curve_template_v"] = strat.oos_curve_template_v
    setup["jcl_version"]          = strat.jcl_version
    setup["symbol"]               = strat.symbol
    setup["chart_series"]         = strat.chart_series
    setup["reopt_param_names"]    = strat.reopt_param_names
    setup["fitness_func"]         = strat.fitness_function
    setup["max_bars_back"]        = strat.max_days_back
    setup["oosPercentLast"]       = 0
    setup["session_num"]          = strat.market_session_id
    setup["session_name"]         = f"session {strat.market_session_id}"
    #setup["start_dt"]            = strat.bt_start_dt
    #setup["end_dt"]              = strat.bt_end_dt
    setup["strategy_file"]        = strat.strategy_file
    setup["strategy_oos_file"]    = strat.strategy_oos_file

    # setup["swfa_done_fn"] = PureWindowsPath(ats_dir_win / jcl_dir)
    # setup["swfa_done_fn"] = PureWindowsPath(
    #    setup["swfa_done_fn"] / f"{cand.wfa_file}.done"
    # )

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
            warn(f"el_block not defined, cand_id={setup['cand_id']}, var={k}")

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


def prepare_data(dbh, data_dir, archive_dir):
    logger.debug(f"prepare_data(dbh, {data_dir}, {archive_dir}):")
    is_file, oos_file = oldest_dp_file_pair(data_dir)
    logger.debug(f"is_file ={is_file}")
    logger.debug(f"oos_file={oos_file}")
    if not is_file or not oos_file:
        return None, None
    is_file = archive_file(archive_dir, is_file)
    oos_file = archive_file(archive_dir, oos_file)

    proto_id = os.path.basename(is_file).split("_")[1]
    logger.debug(f"proto_id={proto_id}")

    df_is = pd.read_csv(is_file, sep="\t", index_col="Test")
    df_oos = pd.read_csv(oos_file, sep="\t", index_col="Test")

    strat_name = [c.split(":")[0] for c in df_is.columns if c.startswith("proto_")][0]

    df_oos.rename(
        columns=lambda n: n.replace(f"{strat_name}: ", "param:"), inplace=True
    )
    df_oos.rename(columns=lambda n: n.replace("All:", "OOS:"), inplace=True)
    df_is.rename(columns=lambda n: n.replace(f"{strat_name}: ", "param:"), inplace=True)
    df_is.rename(columns=lambda n: n.replace("All:", "IS:"), inplace=True)

    df = df_is.join(df_oos.loc[:, df_oos.columns.str.startswith("OOS:")])
    df["IS: NP2DD"] = df["IS: Net Profit"] / -df["IS: Max Intraday Drawdown"]
    df["OOS: NP2DD"] = df["OOS: Net Profit"] / -df["OOS: Max Intraday Drawdown"]

    df["IS: Expectancy"] = df["IS: Avg Winning Trade"] * df[
        "IS: % Profitable"
    ] / 100 - df["IS: Avg Losing Trade"] * (1 - df["IS: % Profitable"] / 100)

    df["OOS: Expectancy"] = df["OOS: Avg Winning Trade"] * df[
        "OOS: % Profitable"
    ] / 100 - df["OOS: Avg Losing Trade"] * (1 - df["OOS: % Profitable"] / 100)

    df["AvgTrade_Filter"] = 0
    df["Quartile"] = 0
    df.sort_values(["IS: TradeStation Index"], ascending=False, inplace=True)

    set_filters(dbh, df, proto_id)

    return proto_id, df


def set_filters(dbh, df, proto_id, filter_list=(F1, F2, F3, F4, F5, F6)):
    logger.debug(f"set_filters(dbh, df, {proto_id}, {filter_list})")
    if F1 in filter_list:
        avg_trade_level = 60
        logger.debug(f"F1 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > 60)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F1)
    if F2 in filter_list:
        logger.debug(f"proto = queryPrototype(dbh, {proto_id})")
        proto = queryPrototype(dbh, proto_id)
        # print(proto)
        slippage, commission = queryCosts(dbh, proto.symbol)
        avg_trade_level = 2 * (slippage + commission)
        logger.debug(f"F2 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > avg_trade_level)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F2)
    if F3 in filter_list:
        proto = queryPrototype(dbh, proto_id)
        slippage, commission = queryCosts(dbh, proto.symbol)
        avg_trade_level = 3 * (slippage + commission)
        logger.debug(f"F3 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > avg_trade_level)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F3)
    if F4 in filter_list:
        proto = queryPrototype(dbh, proto_id)
        # slippage, commission = queryCosts(dbh,proto[0].symbol)
        slippage, commission = queryCosts(dbh, proto.symbol)
        avg_trade_level = 5 * (slippage + commission)
        logger.debug(f"F4 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > avg_trade_level)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F4)
    if F5 in filter_list:
        proto = queryPrototype(dbh, proto_id)
        # slippage, commission = queryCosts(dbh,proto[0].symbol)
        slippage, commission = queryCosts(dbh, proto.symbol)
        avg_trade_level = 6 * (slippage + commission)
        logger.debug(f"F5 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > avg_trade_level)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F5)
    if F6 in filter_list:
        proto = queryPrototype(dbh, proto_id)
        # slippage, commission = queryCosts(dbh,proto[0].symbol)
        slippage, commission = queryCosts(dbh, proto.symbol)
        avg_trade_level = 7 * (slippage + commission)
        logger.debug(f"F6 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > avg_trade_level)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F6)
    if F7 in filter_list:
        proto = queryPrototype(dbh, proto_id)
        # slippage, commission = queryCosts(dbh,proto[0].symbol)
        slippage, commission = queryCosts(dbh, proto.symbol)
        avg_trade_level = 8 * (slippage + commission)
        logger.debug(f"F7 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > avg_trade_level)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F7)
    if F8 in filter_list:
        proto = queryPrototype(dbh, proto_id)
        # slippage, commission = queryCosts(dbh,proto[0].symbol)
        slippage, commission = queryCosts(dbh, proto.symbol)
        avg_trade_level = 9 * (slippage + commission)
        logger.debug(f"F8 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > avg_trade_level)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F8)
    if F9 in filter_list:
        proto = queryPrototype(dbh, proto_id)
        # slippage, commission = queryCosts(dbh,proto[0].symbol)
        slippage, commission = queryCosts(dbh, proto.symbol)
        avg_trade_level = 10 * (slippage + commission)
        logger.debug(f"F9 avg_trade_level={avg_trade_level}")
        df.loc[
            (df["IS: Net Profit"] > 0)
            & (df["OOS: Net Profit"] > 0)
            & (df["IS: Robustness Index"] > 60)
            & (df["IS: Avg Trade"] > avg_trade_level)
            & (df["OOS: Total Trades"] > 10),
            "AvgTrade_Filter",
        ] = (df["AvgTrade_Filter"] | F9)

    logger.debug("Filter Counts ...")
    for f_level in (F10, F9, F8, F7, F6, F5, F4, F3, F2, F1):
        logger.debug(
            f"{Fmap[f_level]} :: {len(df[df['AvgTrade_Filter'] & f_level == f_level])}"
        )


def record_candidates(dbh, proto_id, params):
    logger.debug(f"record_candidates(dbh, {proto_id}, {params}):")
    # if not test_mode:
    add_candidate(dbh, proto_id, params)
    # else:
    #    print("In test mode.")


def add_non_optimized_settings(dbh, proto_id, cand_params):
    logger.debug(f"add_non_optimized_settings(dbh, {proto_id}, {cand_params}):")
    proto_settings = queryPrototypeParams(dbh, proto_id)
    for setting in proto_settings:
        if setting.name not in cand_params.keys():
            if setting.input_type != "var":
                warn(
                    f"add_non_optimized_settings: setting should be var for proto {proto_id} var {setting.name} !!!!"
                )
            continue
            cand_params[setting.name] = setting.value


def parse_row_for_parent_setting(dbh, row, parent_name):
    logger.debug(f"column: param:{parent_name}")
    val = row[f"param:{parent_name}"]
    param_def = queryParamDef(dbh, parent_name)
    if param_def.data_type == "int":
        val = int(val)
    logger.debug("**********************************************")
    logger.debug(f"parse_row_for_parent_setting: {parent_name},  val = {val}")
    logger.debug("**********************************************")
    return val


import re


def param_used_by_parent(dbh, col_name, parent, id):
    logger.debug(f"param_used_by_parent({col_name},{parent},{id})")
    patrn = re.compile("_\d\d*$")
    if re.search(patrn, parent):
        parent, ds = parent.rsplit("_")
    # parent = re.sub( r"_\d*$", "", parent)
    logger.debug(f"param_used_by_parent: {parent}")
    logic = queryLogic(dbh, parent, id)
    logger.debug(f"long_logic: {logic.long_logic}")
    logger.debug(f"short_logic: {logic.short_logic}")
    logger.debug(f"long_params: {logic.long_params}")
    logger.debug(f"short_params: {logic.short_params}")
    if logic.long_params:
        for param in logic.long_params.split(","):
            if col_name == param.format(dn=ds):
                logger.debug(f"filter({id}) uses param {col_name}")
                return True
    if logic.short_params:
        for param in logic.short_params.split(","):
            if col_name == param.format(dn=ds):
                logger.debug(f"filter({id}) uses param {col_name}")
                return True
    logger.debug(f"filter({id}) Does Not use param {col_name}")
    return False


def capture_params(dbh, proto_id, df, top_q=[]):
    filter_col = [col for col in df if col.startswith("param:")]
    cnt = 0
    logger.debug(f"filter_col = {filter_col}<<<<<<")
    for i, j in df.iterrows():
        cand_params = {}
        cand_params["Test"] = i
        hash_keys = []
        logger.debug(f"j={j}")
        for c in filter_col:
            col_name = c.split(":")[1]
            logger.debug(f"col_name={col_name}")
            patrn = re.compile("_n\d\d*$")
            if re.search(
                patrn, col_name
            ):  # and col_name.split('_')[-1].startswith('n'):
                parent = col_name[: col_name.rfind("_")]
                param_num = col_name.split("_")[-1][1:]
                logger.debug(f"parent={parent}")
                logger.debug(f"param_num={param_num}")
                parent_setting = parse_row_for_parent_setting(dbh, j, parent)
                if not param_used_by_parent(dbh, col_name, parent, parent_setting):
                    logger.debug(f"{col_name} is NOT used by {parent} {parent_setting}")
                    continue
            logger.debug(f"add {col_name} to cand_params")
            cand_params[col_name] = j[c]
            logger.debug(cand_params)
            hash_keys.append(str(j[c]))
        hk = ":".join(hash_keys)
        if hk in _param_hash:
            logger.debug("Found duplicate candidate")
            continue
        _param_hash[hk] = 1
        cnt += 1
        cand_params["filters"] = int(j["AvgTrade_Filter"])
        logger.debug("*** 1 ***")
        logger.debug(cand_params)
        cand_params["top_q"] = ",".join(top_q)
        logger.debug("*** 2 ***")
        logger.debug(cand_params)
        add_non_optimized_settings(dbh, proto_id, cand_params)
        logger.debug("*** 3 ***")
        logger.debug(cand_params)
        record_candidates(dbh, proto_id, cand_params)
    return cnt


def select_candidates(dbh, proto_id, df):
    cand_cnt = 0

    # sort by TSI and capture top 10
    cand_df = df.sort_values("IS: TradeStation Index", ascending=False).head(10)
    if len(cand_df) > 0:
        cand_cnt += capture_params(dbh, proto_id, cand_df)

    # print(f"IS: NP2DD = {df[df['IS: NP2DD']>1][['IS: NP2DD','OOS: NP2DD','IS: Total Trades','IS: Net Profit','IS: Max Intraday Drawdown']]}")
    logger.debug(
        f"IS: NP2DD = {df[(df['IS: NP2DD']>2)&(df['OOS: NP2DD']>1)][['IS: NP2DD','OOS: NP2DD','IS: Total Trades','OOS: Total Trades','IS: Net Profit','IS: Max Intraday Drawdown']]}"
    )
    # top_q = ['OOS: Avg Trade|90','IS: Avg Trade|90']
    for f_level in (F10, F9, F8, F7, F6, F5, F4, F3, F2, F1):
        for trade_cnt in (100, 90, 80, 70, 60, 50, 40):
            for np2dd_x in (5, 4, 3, 2):
                top_q = ""  # [f"OOS: Avg Trade|{q_level}", f"IS: Avg Trade|{q_level}"]
                if cand_cnt > 20:
                    logger.debug(
                        f"{top_q}: f_level: {f_level}, trade_cnt: {trade_cnt}: {cand_cnt}"
                    )
                    return cand_cnt
                cand_df = df[
                    (df["AvgTrade_Filter"] & f_level == f_level)
                    & (df["IS: NP2DD"] > np2dd_x)
                    & (df["OOS: NP2DD"] > 1)
                    & (df["IS: Total Trades"] > trade_cnt)
                ]
                if len(cand_df) > 0:
                    cand_cnt += capture_params(dbh, proto_id, cand_df, top_q=top_q)
                logger.debug(
                    f"{top_q}: f_level: {f_level}, trade_cnt: {trade_cnt}: {cand_cnt}"
                )

    """
    # top_q = ['OOS: Avg Trade|90']
    for f_level in (F10, F9, F8, F7, F6, F5, F4, F3, F2, F1):
        for trade_cnt in (100, 90, 80, 70, 60,50):
            for q_level in (90,80,70,60):
                top_q = [f"OOS: Avg Trade|{q_level}"]
                if cand_cnt > 20:
                    logger.debug(
                        f"{top_q}: f_level: {f_level}, trade_cnt: {trade_cnt}: {cand_cnt}"
                    )
                    return cand_cnt
                cand_df = df[
                    (df["AvgTrade_Filter"] & f_level == f_level)
                    & (df["IS: Total Trades"] > trade_cnt)
                    & (
                        df["OOS: Avg Trade"]
                        >= df["OOS: Avg Trade"].quantile(q_level / 100.0)
                    )
                ]
                cand_cnt += capture_params(dbh, proto_id, cand_df, top_q=top_q)
                logger.debug(f"{top_q}: f_level: {f_level}, trade_cnt: {trade_cnt}: {cand_cnt}")
    """

    return cand_cnt


def generateStrategyCode(dbh, setup):
    logic = {}
    desc = formatCommentStrings(setup)
    hdr = setHeader(setup)

    logic["lsb"] = lsbLogic(setup)
    logic["poi"] = poiLogic(dbh, setup)
    logic["filters"] = filterLogic(dbh, setup)
    logic["tseg"] = timeSegmentLogic(setup)
    logic["stop_loss"] = stopLossLogic(setup)
    logic["profit_target"] = profitTargetLogic(setup)

    logger.debug(logic)
    pprint.pprint(logic)

    if not good_logic(logic):
        warn("Not Good Logic")
        return None

    logger.debug(setup)
    pprint.pprint(setup)

    strat = processStrategyTemplate(hdr, desc, setup, logic)

    logger.debug(f"write Strategy to {setup['strategy_file']}")
    open(setup["strategy_file"], "w").write(strat)
    return strat


def generateJclCode(dbh, setup):
    code = processJclTemplate(setup)
    logger.debug(f"write JCL to {setup['jcl_file']}")
    open(setup["jcl_file"], "w").write(code)
    return code


def parse_oos_report(fn):
    logger.debug(f"parse_oos_report({fn}):")
    # print(fn.read_text())
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
                """
                print(f"run        ={run}")
                print(f"start_dt   ={start_dt}")
                print(f"end_dt     ={end_dt}")
                print(f"days       ={days}")
                print(f"bars       ={bars}")
                print(f"net profit ={np}")
                print(f"max DD       ={dd}")
                print(f"max DD %       ={ddp}")
                print(f"num trades       ={nt}")
                print(f"% prof       ={pp}")
                print(f"avg w/l       ={wl}")
                print(f"avg trade       ={at}")
                print(f"std dev       ={sd}")
                print(f"median       ={med}")
                print(f"profit fact  ={pf}")
                print(f"risk-reward  ={rrr}")
                print(f"t-Test       ={tt}")
                print(f"params       ={params}")
                """
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
    start_dt: str = ""
    end_dt: str = ""
    name: str = ""
    value: str = ""
    status: str = ""
    data_type: str = ""

def get_historical_params(dbh, setup, cand_id, strat_id):
    print(f"{rpt_dir}/*_cand-{cand_id}/*cand-{cand_id}*_OOS*.txt")
    oos_fn = glob.glob(f"{rpt_dir}/*_cand-{cand_id}/*cand-{cand_id}*_OOS*runs.txt")[0]
    df_oos = parse_oos_report(oos_fn)

    var_names = []
    data_types = []
    for rec in  setup["reopt_param_names"].split(','):
        n, t = rec.split(':')
        var_names.append(n)
        data_types.append(t)

    setup["oos_curve_params"] = ""
    setup["start_dt"] = None
    for i, row in df_oos.iterrows():
        ys, ms, ds = row.start_dt.split("/")
        ye, me, de = row.end_dt.split("/")
        if int(ds) == 0:
            ds = "01"
        if int(de) == 0:
            de = "01"

        start_dt = f"{ms}/{ds}/{ys}"
        end_dt   = f"{me}/{de}/{ye}"
        if not setup["start_dt"]:
            setup["start_dt"] = start_dt
        setup["end_dt"] = end_dt

        setup["oos_curve_params"] += f"if date >= ELDate({ms},{ds},{ys}) and date < ELDate({me},{de},{ye}):\n"

        for i, p in enumerate(row.Parameters.split(",")):
            setup["oos_curve_params"] += f"    {var_names[i]} = {p};\n"

            setting = Setting()
            setting.start_dt = start_dt,
            setting.end_dt   = end_dt,
            setting.name     = var_names[i],
            setting.data_type = data_types[i],
            setting.value    = p,
            setting.status   = "past",
            logger.debug(f"setting: {setting}")
            dbInsertStrategySetting(dbh, strat_id, setting)


'''
def format_strategy_historical_params(dbh, setup, strat_id):
    logger.debug(f"format_strategy_historical_params(dbh,{strat_id}):")

    var_names = []
    for param in queryStrategyParams(dbh, cand_id):
        var_names.append(param.name)
    logger.debug(f"var_names={var_names}")

    str = ""
    for f in rpt_dir.glob("*.txt"):
        if "_OOS" in f.stem and "OverallResult" not in f.stem:
            df_oos = parse_oos_report(f)
            for i, row in df_oos.iterrows():
                str += f"if date >= {row.start_dt} and date < {row.end_dt}:\n"
                for i, p in enumerate(row.Parameters.split(",")):
                    str += f"    {var_names[i]} = {p};\n"
    return str
'''


def run_strategy_setup():
    dbh = connectDB()
    strat_id = nextStrategyId(dbh)
    if not strat_id:
        return None
    cand_id = queryStrategy(dbh, strat_id).cand_id
    run_update_strategy_reopt_parameters(dbh, strat_id, cand_id)
    setup = getStrategySetup(dbh, strat_id)

    clear_strategy_settings(dbh,strat_id)
    clear_strategy_parameters(dbh,strat_id)

    run_update_strategy_settings(dbh, strat_id, cand_id)
    #setup["oos_curve_params"] = format_strategy_historical_params(dbh, setup, strat_id)
    get_historical_params(dbh, setup, cand_id, strat_id)

    with open(f"{json_dir}/strat_{strat_id}.json",'w') as json_file:
        json.dump(setup, json_file)
    run_generate_code(dbh, setup)


def run_update_strategy_settings(dbh, strat_id, cand_id):
    for setting in queryCandidateSettings(dbh, cand_id):
        setting.status = "fixed"
        setting.start_dt = None
        setting.end_dt = None
        dbInsertStrategySetting(dbh, strat_id, setting)
    dbUpdateStrategy(dbh, strat_id, {"status": "Strategy", "status_state": "settings"})


def run_update_strategy_reopt_parameters(dbh, strat_id, cand_id):
    reopt_param_names = queryCandidate(dbh, cand_id).reopt_param_names
    dbUpdateStrategy(dbh, strat_id, {"reopt_param_names": reopt_param_names})
    
    for param in queryCandidateParams(dbh, cand_id):
        dbInsertStrategyParams(dbh, strat_id, param)
    dbUpdateStrategy(dbh, strat_id, {"status": "Strategy", "status_state": "reopt_params"})


def run_generate_code(dbh, setup):
    logger.debug(f"processing strategy: {setup['strat_id']}")

    ##  testing code
    # cand_id = '333'
    # logger.debug(f"*********** cand_id: {cand_id}")
    # setup = getCandidateSetup(dbh, cand_id)
    # logger.debug("************************************************")
    # logger.debug(setup)
    # pprint.pprint(setup)
    # logger.debug("************************************************")
    # generateCandidateCode(dbh, setup)
    # logger.debug("************************************************")
    # exit()

    cnt = 0
    cnt += 1
    #setup = getStrategySetup(dbh, strat_id)
    print("Setup ...")
    pprint.pprint(setup)
    exit()

    if not generateStrategyCode(dbh, setup):
        logger.debug("could not generate strategy code for strat_id {setup['strat_id']}")
        return None

    if not generateJclCode(dbh, setup):
        logger.debug("could not generate jcl code for strat_id {setup['strat_id']}")
        return None

    dbUpdateStrategy(dbh, setup['strat_id'], {"status": "code", "status_state": "done"})
