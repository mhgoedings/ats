import sys
import os
import platform
from pathlib import Path, PureWindowsPath
from loguru import logger

import pprint

from config_vars import ats_dir, warn, ats_dir_win, jcl_dir, cand_code_dir, jcl_code_dir

import pandas as pd

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
from data_prep_tools import setSessionVars, setDataSeries
from ats_template_tools import formatCommentStrings, setHeader
from db_query import connectDB, queryPrototype, queryCosts, queryPrototypeParams
from db_query import (
    nextCandidateId,
    queryCandidate,
    queryCandidateSettings,
    queryCandidateParams,
    queryLogic,
    queryParamDef,
)
from db_insert_update import dbUpdateCandidate
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
Fmap = { F1: 'F1',
         F2: 'F2',
         F3: 'F3',
         F4: 'F4',
         F5: 'F5',
         F6: 'F6',
         F7: 'F7',
         F8: 'F8',
         F9: 'F9',
         F10: 'F10',
       }



def getCandidateSetup(dbh, cand_id):
    logger.debug(f"cand_id = {cand_id}")
    cand = queryCandidate(dbh, cand_id)
    proto = queryPrototype(dbh, cand.proto_id)
    settings = queryCandidateSettings(dbh, cand_id)
    params = queryCandidateParams(dbh, cand_id)

    setup = {}
    setup["proto_id"] = proto.id
    setup["cand_id"] = cand_id
    setup["template_version"] = cand.template_version
    setup["jcl_version"] = cand.jcl_version
    setup["symbol"] = proto.symbol
    setup["data_set"] = proto.data_set
    setup["data_block"] = proto.data_block
    setup["chart_series"] = proto.chart_series
    setup["fitness_func"] = proto.fitness_function
    setup["max_bars_back"] = proto.max_days_back
    setup["oosPercentLast"] = 0
    setup["session_num"] = proto.market_session_id
    setup["session_name"] = f"session {proto.market_session_id}"
    setup["start_dt"] = proto.bt_start_dt
    setup["end_dt"] = proto.bt_end_dt
    setup["walk_forward_file"] = cand.wfa_file

    setup["swfa_done_fn"] = PureWindowsPath(ats_dir_win / jcl_dir)
    setup["swfa_done_fn"] = PureWindowsPath(setup["swfa_done_fn"] / f"{cand.wfa_file}.done")

    setup["sess_start"], setup["sess_end"] = setSessionVars(dbh, setup["session_num"])
    setup["data_series"] = setDataSeries(setup["chart_series"])

    setup["vars"] = {}
    setup["counts"] = {}
    setup["counts"]["el_vars"] = 0
    setup["counts"]["el_inputs"] = 0
    setup["counts"]["data_series"] = 0

    setup["opt_inputs"] = {}
    setup["var_names"] = []
    setup["input_names"] = []
    setup["param_vars"] = {}

    logger.debug("========= for s in settings:")
    for s in settings:
        logger.debug(f"settings:  s={s.name}")
        #setup["param_vars"][s.name] = {"d_type": s.data_type, "value": s.value}
        setup["vars"].setdefault(s.name, {})["d_type"] = s.data_type
        setup["vars"][s.name]["setting"] = s.value
        logger.debug(f"setup['vars'][{s.name}]['setting'] = {s.value}")
        setup["vars"][s.name]["el_block"] = "variable"
        setup["var_names"].append(s.name)
        setup["counts"]["el_vars"] += 1
        logger.debug(setup["vars"][s.name])

    logger.debug("========= for p in params:")
    param_order = []
    for p in params:
        logger.debug(f"params:  p={p.name}")
        param_name, param_setup = parseInput(p)
        setup["opt_inputs"][param_name] = param_setup
        param_order.append(f"{param_name}:{param_setup['dtype']}")
        pprint.pprint(param_setup)
        setup["vars"][param_name]["dtype"] = param_setup['dtype']
        if param_setup["type"] == "var":
            logger.debug("========= var:")
            setup["vars"][param_name]["setting"] = p.value
            setup["vars"][param_name]["el_block"] = "variable"
            setup["var_names"].append(param_name)
            setup["counts"]["el_vars"] += 1
        else:
            logger.debug("========= else:")
            setup["vars"][param_name]["el_block"] = "input"
            setup["input_names"].append(param_name)
            setup["counts"]["el_inputs"] += 1
            logger.debug(setup['vars'][param_name])
        logger.debug(setup["vars"][param_name])
    setup["reopt_param_names"] = ",".join(param_order)
    dbUpdateCandidate(dbh, cand_id, {"reopt_param_names": setup["reopt_param_names"]})

    '''
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
    '''

    '''
    for k, v in setup["vars"].items():
        logger.debug(f"items:  {v}")
        pprint.pprint(f"*getCandidateSetup: items:  {v}")
        if v["el_block"] == "input":
            setup["input_names"].append(k)
        elif v["el_block"] == "variable":
            setup["var_names"].append(k)
        else:
            warn(f"el_block not defined, cand_id={setup['cand_id']}, var={k}")
    '''

    setup["timeframes"] = []
    for ds in setup["chart_series"].split(","):
        i, symbol, tf, unit = ds.split(":")
        tf_d = {"ds": i, "symbol": symbol, "tf": tf, "unit": unit}
        setup["timeframes"].append(tf_d)
        setup["counts"]["data_series"] += 1

    dir = f"{ats_dir}/Data/CandidateCode/"
    if platform.system() == 'Windows':
        dir = str(PureWindowsPath(ats_dir_win / cand_code_dir))

    setup["strategy_name"] = f"cand_{cand_id}"
    setup["strategy_file"] = f"{dir}/{setup['strategy_name']}"

    dir = f"{ats_dir}/Data/OptimizationApiCode/"
    if platform.system() == 'Windows':
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
        #print(proto)
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
        logger.debug(f"{Fmap[f_level]} :: {len(df[df['AvgTrade_Filter'] & f_level == f_level])}")



def record_candidates(dbh, proto_id, params):
    logger.debug(f"record_candidates(dbh, {proto_id}, {params}):")
    #if not test_mode:
    add_candidate(dbh, proto_id, params)
    #else:
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


def parse_row_for_parent_setting(dbh,row,parent_name):
    logger.debug(f"column: param:{parent_name}")
    val = row[f'param:{parent_name}']
    param_def = queryParamDef(dbh, parent_name)
    if param_def.data_type == "int":
        val = int(val)
    logger.debug("**********************************************")
    logger.debug(f"parse_row_for_parent_setting: {parent_name},  val = {val}")
    logger.debug("**********************************************")
    return val

import re
def param_used_by_parent(dbh,col_name,parent,id):
    logger.debug(f"param_used_by_parent({col_name},{parent},{id})")
    patrn = re.compile('_\d\d*$')
    if re.search(patrn, parent):
        parent,ds = parent.rsplit('_')
    #parent = re.sub( r"_\d*$", "", parent)
    logger.debug(f"param_used_by_parent: {parent}")
    logic = queryLogic(dbh, parent, id)
    logger.debug(f"long_logic: {logic.long_logic}")
    logger.debug(f"short_logic: {logic.short_logic}")
    logger.debug(f"long_params: {logic.long_params}")
    logger.debug(f"short_params: {logic.short_params}")
    if logic.long_params:
        for param in logic.long_params.split(','):
            if col_name == param.format(dn=ds):
                logger.debug(f"filter({id}) uses param {col_name}")
                return True
    if logic.short_params:
        for param in logic.short_params.split(','):
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
            patrn = re.compile('_n\d\d*$')
            if re.search(patrn, col_name):  # and col_name.split('_')[-1].startswith('n'):
                parent = col_name[:col_name.rfind('_')]
                param_num = col_name.split('_')[-1][1:]
                logger.debug(f"parent={parent}")
                logger.debug(f"param_num={param_num}")
                parent_setting =  parse_row_for_parent_setting(dbh,j,parent)
                if not param_used_by_parent(dbh,col_name,parent,parent_setting):
                    logger.debug(f"{col_name} is NOT used by {parent} {parent_setting}")
                    continue;
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
    cand_df = df.sort_values('IS: TradeStation Index', ascending=False).head(10)
    if len(cand_df) > 0:
        cand_cnt += capture_params(dbh, proto_id, cand_df)

    #print(f"IS: NP2DD = {df[df['IS: NP2DD']>1][['IS: NP2DD','OOS: NP2DD','IS: Total Trades','IS: Net Profit','IS: Max Intraday Drawdown']]}") 
    logger.debug(f"IS: NP2DD = {df[(df['IS: NP2DD']>2)&(df['OOS: NP2DD']>1)][['IS: NP2DD','OOS: NP2DD','IS: Total Trades','OOS: Total Trades','IS: Net Profit','IS: Max Intraday Drawdown']]}") 
    # top_q = ['OOS: Avg Trade|90','IS: Avg Trade|90']
    for f_level in (F10, F9, F8, F7, F6, F5, F4, F3, F2, F1):
        for trade_cnt in (100,90,80,70,60,50,40):
            for np2dd_x in (5,4,3,2):
                top_q = ''  #[f"OOS: Avg Trade|{q_level}", f"IS: Avg Trade|{q_level}"]
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
                logger.debug(f"{top_q}: f_level: {f_level}, trade_cnt: {trade_cnt}: {cand_cnt}")

    '''
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
    '''

    return cand_cnt


def generateCandidateCode(dbh, setup):
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

    logger.debug(f"write Candidate to {setup['strategy_file']}")
    open(setup["strategy_file"], "w").write(strat)
    return strat


def generateJclCode(dbh, setup):
    code = processJclTemplate(setup)
    logger.debug(f"write JCL to {setup['jcl_file']}")
    open(setup["jcl_file"], "w").write(code)
    return code


def run_filter(data_dir, archive_dir):
    dbh = connectDB()
    proto_id, df = prepare_data(dbh, data_dir, archive_dir)
    if not proto_id:
        return proto_id
    #test_mode = True
    cnt = select_candidates(dbh, proto_id, df)
    exit()
    # generateCandidateCode(dbh, proto_id)
    return cnt


def run_test(cand_id='1725'):
    dbh = connectDB()
    ##  testing code
    logger.debug(f"*********** cand_id: {cand_id}")
    setup = getCandidateSetup(dbh, cand_id)
    logger.debug("************************************************")
    logger.debug(setup)
    pprint.pprint(setup)
    logger.debug("************************************************")
    generateCandidateCode(dbh, setup)
    logger.debug("************************************************")
    exit()


def run_generate_code():
    dbh = connectDB()
    cand_id = nextCandidateId(dbh)
    logger.debug(f"processing candidate: {cand_id}")
    if not cand_id:
        logger.debug("No candidate returned")
        return cand_id

    ##  testing code
    #cand_id = '1725'
    #logger.debug(f"*********** cand_id: {cand_id}")
    #setup = getCandidateSetup(dbh, cand_id)
    #logger.debug("************************************************")
    #logger.debug(setup)
    #pprint.pprint(setup)
    #logger.debug("************************************************")
    #generateCandidateCode(dbh, setup)
    #logger.debug("************************************************")
    #exit()

    cnt = 0
    while cand_id:
        cnt += 1
        setup = getCandidateSetup(dbh, cand_id)

        if not generateCandidateCode(dbh, setup):
            logger.debug("could not generate candidate code for cand_id {cand_id}")
            return None

        if not generateJclCode(dbh, setup):
            logger.debug("could not generate jcl code for cand_id {cand_id}")
            return None

        dbUpdateCandidate(dbh, cand_id, {"status": "code", "status_state": "done"})
        cand_id = nextCandidateId(dbh)

    return cnt
