import pandas as pd
import sys
import os
from loguru import logger

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
from config_vars import warn, ats_dir, ats_dir_win, dp_dir, jcl_dir, PureWindowsPath, Path

from db_query import connectDB, queryPrototype, queryPrototypeParams, nextPrototypeId
from db_insert_update import dbUpdatePrototype

from data_prep_tools import formatDate, setSessionVars, setDataSeries
from ats_template_tools import formatCommentStrings, setHeader
from ats_template_tools import parseInput, lsbLogic, poiLogic, filterLogic
from ats_template_tools import timeSegmentLogic, stopLossLogic, profitTargetLogic
from ats_template_tools import processStrategyTemplate, processJclTemplate


def getPrototypeSetup(dbh, id):
    proto = queryPrototype(dbh, id)
    params = queryPrototypeParams(dbh, id)
    setup = {}
    setup["proto_id"] = proto.id
    setup["template_version"] = proto.template_version
    setup["jcl_version"] = proto.jcl_version
    setup["symbol"] = proto.symbol
    setup["data_set"] = proto.data_set
    setup["data_block"] = proto.data_block
    setup["chart_series"] = proto.chart_series
    setup["fitness_func"] = proto.fitness_function
    setup["max_bars_back"] = proto.max_days_back
    setup["oosPercentLast"] = 20
    setup["session_num"] = proto.market_session_id
    setup["session_name"] = f"session {proto.market_session_id}"
    setup["prestart_dt"] = formatDate(proto.prestart_dt)
    setup["start_dt"] = formatDate(proto.start_dt)
    setup["end_dt"] = formatDate(proto.end_dt)

    setup["gao_done_fn"] = PureWindowsPath(ats_dir_win / jcl_dir)
    setup["gao_done_fn"] = PureWindowsPath(setup["gao_done_fn"] / f"proto_{proto.id}.done")

    setup['in_sample_file'] = PureWindowsPath(ats_dir_win / dp_dir / proto.in_sample_file)
    setup['out_of_sample_file'] = PureWindowsPath(ats_dir_win / dp_dir / proto.out_of_sample_file)

    logger.debug(f"in_sample_file = {setup['in_sample_file']}")
    logger.debug(f"out_of_sample_file = {setup['out_of_sample_file']}")

    setup["sess_start"], setup["sess_end"] = setSessionVars(dbh, setup["session_num"])
    setup["data_series"] = setDataSeries(setup["chart_series"])

    setup["opt_inputs"] = {}
    setup["param_vars"] = {}
    setup["vars"] = {}
    for p in params:
        param_name, param_setup = parseInput(p)
        setup["opt_inputs"][param_name] = param_setup
    setup['num_tests'] = count_tests(setup["opt_inputs"])
    setup["timeframes"] = []
    for ds in setup["chart_series"].split(","):
        i, symbol, tf, unit = ds.split(":")
        tf_d = {"ds": i, "symbol": symbol, "tf": tf, "unit": unit}
        setup["timeframes"].append(tf_d)

    dir = f"{ats_dir}/Data/OptimizationApiCode"
    setup["jcl_file"] = f"{dir}/proto_{setup['proto_id']}.jcl"
    dir = f"{ats_dir}/Data/PrototypeCode"
    setup["strategy_name"] = f"proto_{setup['proto_id']}"
    setup["strategy_file"] = f"{dir}/{setup['strategy_name']}"

    return setup


def count_tests(params):
    logger.debug("============> count_tests")
    cnt = 1
    for k,v in params.items():
        cnt *= len(v['value'])
        logger.debug(f"{k}   len={len(v['value'])}   cnt={cnt}")
    return cnt

#import pprint
def good_logic(logic):
    if not logic["lsb"] or len(logic["lsb"])==0:
        #pprint.pprint(f"lsb :{logic['lsb']}")
        pass
    if not logic["poi"] or len(logic["poi"])==0:
        #pprint.pprint(f"poi :{logic['poi']}")
        return None
    if not logic["filters"] or len(logic["filters"])==0:
        #pprint.pprint(f"filters :{logic['filters']}")
        return None
    if not logic["tseg"] or len(logic["tseg"])==0:
        #pprint.pprint(f"tseg :{logic['tseg']}")
        return None
    if not logic["stop_loss"] or len(logic["stop_loss"])==0:
        #pprint.pprint(f"stop_loss :{logic['stop_loss']}")
        pass
    if not logic["profit_target"] or len(logic["profit_target"])==0:
        #pprint.pprint(f"profit_target :{logic['profit_target']}")
        pass
    return True

def generatePrototypeCode(dbh, setup):
    logic = {}
    desc = formatCommentStrings(setup)
    hdr = setHeader(setup)

    logic["lsb"] = lsbLogic(setup)
    logic["poi"] = poiLogic(dbh, setup) 
    logic["filters"] = filterLogic(dbh, setup)
    logic["tseg"] = timeSegmentLogic(setup)
    logic["stop_loss"] = stopLossLogic(setup)
    logic["profit_target"] = profitTargetLogic(setup)

    if not good_logic(logic):
        return None

    strat = processStrategyTemplate(hdr, desc, setup, logic)

    logger.debug(f"write Proto to {setup['strategy_file']}")
    open(setup["strategy_file"], "w").write(strat)
    return strat


def generateJclCode(dbh, setup):
    code = processJclTemplate(setup)
    logger.debug(f"write JCL to {setup['jcl_file']}")
    open(setup["jcl_file"], "w").write(code)
    return code


def run_generate_code():
    dbh = connectDB()
    proto_id = nextPrototypeId(dbh)
    logger.debug(f"processing prototype: {proto_id}")
    if not proto_id:
        logger.debug("No prototype returned")
        return proto_id

    cnt = 0
    while proto_id:
        cnt += 1
        setup = getPrototypeSetup(dbh,proto_id)

        logger.debug("setup ==>")
        logger.debug(setup)
        if not generatePrototypeCode(dbh,setup):
            logger.debug("could not generate prototype code for proto_id {proto_id}")
            return None

        if setup['num_tests'] < 12500:
            setup['jcl_version'] = f"{setup['jcl_version']}_exhaustive"
            dbUpdatePrototype(dbh, proto_id, {'jcl_version': setup['jcl_version']})
        if not generateJclCode(dbh,setup):
            logger.debug("could not generate jcl code for proto_id {proto_id}")
            return None

        dbUpdatePrototype(dbh, proto_id, {'status': 'code', 'status_state': 'done'})
        proto_id = nextPrototypeId(dbh)

    return cnt



