import numpy as np
from loguru import logger

from glom import glom
from jinja2 import FileSystemLoader, Environment

from config_vars import warn, ats_dir, ats_dir_win, strat_tplt_dir, jcl_tplt_dir
from db_query import queryEntryFilter

from pathlib import Path, PureWindowsPath
import platform
import sys
import os

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
from db_query import queryPoi
from ats_tools import hhmm2mins, add2hhmm


def setHeader(setup):
    return f"""      prototype: { setup['proto_id'] }
      template: { setup['template_version'] }
      job file: { setup['jcl_file'] }
      poi IDs     : { glom(setup,'opt_inputs.poi.value',default=None) }
      filter 1 IDs: { glom(setup,'opt_inputs.filter_1.value',default=None) }
      filter 2 IDs: { glom(setup,'opt_inputs.filter_2.value',default=None) }"""


def formatCommentStrings(setup):
    tf_arr = []
    for tf in setup["timeframes"]:
        tf_arr.append(f"Timeframe-{tf['ds']} = {tf['tf']} {tf['unit']}")
    tf_str = ("\n").join(tf_arr)
    desc = {}
    desc[
        "chart_setup"
    ] = f"""Chart Setup:
      symbol           = {setup['symbol']}
      {tf_str}
      Fitness Function = {setup['fitness_func']}
      maxBarsBack      = {setup['max_bars_back']}
      session name     = {setup['session_name']}
      start date       = {setup['start_dt']}
      end date         = {setup['end_dt']}"""
    desc[
        "prototype_info"
    ] = f"""Prototype Info::
      dataSet = {setup['data_set']}
      dataBlock = {setup['data_block']}"""

    return desc


def addInputRange(p):
    inp_def = {}
    inp_def["type"] = "range"
    inp_def["dtype"] = p.data_type
    inp_def["params"] = p.value
    if p.data_type == "double":
        st, end, step = [float(x) for x in p.value.split(",")]
        inp_def["value"] = [format(x, ".2f") for x in np.arange(st, end + step, step)]
    else:
        st, end, step = [int(x) for x in p.value.split(",")]
        inp_def["value"] = [int(x) for x in np.arange(st, end + step, step)]
    logger.debug(f"addInputRange: inp_def={inp_def}")
    return inp_def


def addInputList(p):
    inp_def = {}
    inp_def["type"] = "list"
    inp_def["dtype"] = p.data_type
    inp_def["value"] = [int(x) for x in p.value.split(",")]
    return inp_def


def addInputVar(p):
    inp_def = {}
    inp_def["type"] = "var"
    inp_def["dtype"] = p.data_type
    inp_def["value"] = [p.value]
    return inp_def


def parseInput(param):
    logger.debug(f"parseInput({param.input_type}):")
    logger.debug(f"parseInput({param.value}):")
    if param.input_type == "range":
        return param.name, addInputRange(param)
    elif param.input_type == "list":
        return param.name, addInputList(param)
    elif param.input_type == "var":
        return param.name, addInputVar(param)
    else:
        warn(f"input_type({param.input_type}) not coded for, id={param.id}")


def filterLogic(dbh, setup):
    filters = {}
    ds = 1
    while True:
        ids = glom(setup, f"opt_inputs.filter_{ds}.value", default=None)
        if not ids:
            logger.debug(f"No filter logic found for opt_inputs.filter_{ds}")
            ids = glom(setup, f"param_vars.filter_{ds}.value", default=None)
        # new logic: candidate
        if not ids:
            ids = glom(setup, f"vars.filter_{ds}.setting", default=None)
            logger.debug(f"filter = {ids}")
        if ids is None:
            logger.debug(f"No filter logic found for param_vars.filter_{ds}")
            break
        if isinstance(ids, str):
            ids = ids.split(",")
        idx = 1
        filters[ds] = {}
        for id in ids:
            q = queryEntryFilter(dbh, id)
            try:
                long_code = q.long_logic.format(
                    p1=f"filter_{ds}_n1", p2=f"filter_{ds}_n2", fn=ds
                )
            except AttributeError:
                long_code = None
            try:
                short_code = q.short_logic.format(
                    p1=f"filter_{ds}_n1",
                    p2=f"filter_{ds}_n2",
                    long=f"{long_code}",
                    fn=ds,
                )
            except AttributeError:
                short_code = None

            # d_filter = {'fid': id,
            #            'long': long_code,
            #            'short': short_code}

            if q.vars:
                for v in q.vars.split(";"):
                    logger.debug(f"for v is {v}")
                    name, dtype, value = v.split(":")
                    # setup["param_vars"][name] = {"d_type": dtype, "value": value}
                    setup["vars"][name] = {"d_type": dtype, "setting": value}

            filters[ds][idx] = {"fid": id, "long": long_code, "short": short_code}
            idx += 1

        ds += 1
    return filters


def lsbLogic(setup):
    if glom(setup, "opt_inputs.lsb.value", default=None) != 4:
        return
    setup["opt_inputs"]["lsb"]["value"] = 3
    logic = f"""
        switch(dow)
        begin
            case 1:
                lsb = mon_lsb;
            case 2:
                lsb = tue_lsb;
            case 3:
                lsb = wed_lsb;
            case 4:
                lsb = thu_lsb;
            case 5:
                lsb = fri_lsb;
        end;
    """
    return logic


def poiLogic(dbh, setup):
    logger.debug("================= poiLogic")
    logger.debug(setup)
    pprint.pprint(setup)
    id_list = glom(setup, "opt_inputs.poi.value", default=None)
    logger.debug(f"id_list = {id_list}")
    if not id_list:
        id_list = glom(setup, "param_vars.poi.value", default=None)
        logger.debug(f"not id_list:  {id_list}")
    # new logic: candidate
    if not id_list:
        id_list = glom(setup, "vars.poi.setting", default=None)
        logger.debug(f"poi id = {id_list}")
    logic = []
    if id_list == "" or id_list == None:
        return logic
    ids = id_list
    if isinstance(id_list, str):
        logger.debug("id_list is a str")
        ids = id_list.split(",")
    if len(ids) == 0:
        return []
    for id in ids:
        logger.debug(f"for id is{id}")
        q = queryPoi(dbh, id)
        if not q:
            # logic = None
            warn(f"poiLogic: No POI logic for id: {id}")
            continue
        logger.debug("append to logic")
        logic.append(
            {
                "poi_id": id,
                "common": q.common_logic,
                "long": q.long_logic,
                "short": q.short_logic,
            }
        )
        logger.debug("check vars")
        if q.vars:
            for v in q.vars.split(";"):
                logger.debug(f"for v is {v}")
                name, dtype, value = v.split(":")
                # setup["param_vars"][name] = {"d_type": dtype, "value": value}
                setup["vars"][name] = {
                    "d_type": dtype,
                    "setting": value,
                    "el_block": "variable",
                }

                #'opt_inputs': {'filter_1': {'dtype': 'int',
                #             'type': 'distinct',
                #             'value': [2, 5, 6]},

    return logic


def calcTimeSegmentSize(start, end, n_segs=3):
    return (hhmm2mins(end) - hhmm2mins(start)) / n_segs


def timeSegmentLogic(setup):
    seg = glom(setup, "opt_inputs.time_segment.value", default=None)
    if not seg:
        seg = glom(setup, "param_vars.time_segment.value", default=None)
    # new logic: candidate
    if not seg:
        seg = glom(setup, "vars.time_segment.setting", default=None)
    tseg = calcTimeSegmentSize(setup["sess_start"], setup["sess_end"])
    timeframe = int(setup["timeframes"][0]["tf"])
    sess_start = setup["sess_start"]
    sess_end = setup["sess_end"]

    if len(seg) > 1:
        code = f"""
        Switch (time_segment) begin
          case 0: begin
            time_filter = True;
          end;
          case 1 : begin
            time_filter = time > {sess_start} and time <= {add2hhmm(sess_start, tseg)};
          end;
          case 2 : begin
            time_filter = time > {add2hhmm(sess_start, tseg)} and time <= {add2hhmm(sess_start, (2*tseg) )};
          end;
          case 3 : begin
            time_filter = time > {add2hhmm(sess_start, (2*tseg))} and time < {add2hhmm(sess_end,-timeframe)};
          end;
        end;
        """
    elif len(seg) == 1:
        if seg[0] == "0":
            code = f"time_filter = True;"
        elif seg[0] == "1":
            code = f"time_filter = time > {sess_start} and time <= {add2hhmm(sess_start, tseg)};"
        elif seg[0] == "2":
            code = f"time_filter = time > {add2hhmm(sess_start, tseg)} and time <= {add2hhmm(sess_start, (2*tseg) )};"
        elif seg[0] == "3":
            code = f"time_filter = time > {add2hhmm(sess_start, (2*tseg))} and time < {add2hhmm(sess_end,-timeframe)};"
        else:
            warn(f"timeSegmentLogic({seg}) NOT CODED")
    else:
        code = f"time_filter = True;"

    return code


def stopLossLogic(setup):
    param = glom(setup, "opt_inputs.stop_loss.value", default=None)
    if param == None:
        return None
    code = "SetStopLoss(stop_loss);"
    return code


def profitTargetLogic(setup):
    param = glom(setup, "opt_inputs.profit_target.value", default=None)
    if param == None:
        return None
    if setup:
        code = "SetProfitTarget(profit_target);"
    return code


import pprint


def processStrategyTemplate(template, hdr, desc, setup, logic):
    logger.debug("processStrategyTemplate ....")
    search_path = f"{ats_dir}/Code/Templates/Strategy/"
    if platform.system() == "Windows":
        search_path = str(PureWindowsPath(ats_dir_win / strat_tplt_dir))
    templateLoader = FileSystemLoader(searchpath=search_path)
    templateEnv = Environment(loader=templateLoader)
    TEMPLATE_FILE = template
    logger.debug(f"process template: {TEMPLATE_FILE}")
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(
        header=hdr,
        chart_setup=desc["chart_setup"],
        prototype_info=desc["prototype_info"],
        # dp_data=dp,
        comments=desc,
        poi="more testing for poi",
        filters=logic["filters"],
        setup=setup,
        logic=logic,
    )
    return outputText


def processJclTemplate(setup):
    # setup['in_sample_file'] = PureWindowsPath(ats_dir_win / dp_dir / setup['in_sample_file'])
    # setup['out_of_sample_file'] = PureWindowsPath(ats_dir_win / dp_dir / setup['out_of_sample_file'])

    search_path = f"{ats_dir}/Code/Templates/JCL/"
    logger.debug(f"platofrm = {platform.system()}")
    if platform.system() == "Windows":
        search_path = str(PureWindowsPath(ats_dir_win / jcl_tplt_dir))
    logger.debug(f"search_path={search_path}")
    templateLoader = FileSystemLoader(searchpath=search_path)
    # templateLoader = FileSystemLoader(searchpath=f"{ats_dir}/Code/Templates/JCL/")
    templateEnv = Environment(loader=templateLoader)
    TEMPLATE_FILE = setup["jcl_version"]
    logger.debug(f"JCL template file: {TEMPLATE_FILE}")
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(
        setup=setup,
        # in_sample_file=in_sample_file,
        # out_of_sample_file=out_of_sample_file,
    )
    return outputText
