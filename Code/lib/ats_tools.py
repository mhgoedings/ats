import math
import numpy as np
import pandas as pd
from random import randint
from loguru import logger

from db_query import (
    querySecId,
    queryDefaultSessionId,
    querySession,
    queryEntryFilter,
    queryPrototype,
    queryPrototypeParams,
    queryParamDef,
    queryParamPreset,
)
from db_insert_update import dbUpdatePrototype, dbUpdateCandidate

import sys

from prototype import Prototype
from prototype_parameter import PrototypeParameter
from candidate import Candidate
from candidate_parameter import CandidateParameter
from candidate_setting import CandidateSetting

from config_vars import warn


def initDataSets():
    data_sets = []
    data_sets.append([1, "1/1/08", "1/1/18"])
    data_sets.append([2, "1/1/08", "7/1/18"])
    data_sets.append([3, "7/1/08", "7/1/18"])
    df = pd.DataFrame(data_sets, columns=["data_set", "start_dt", "end_dt"])
    df.set_index("data_set", inplace=True)
    df["start_dt"] = pd.to_datetime(df["start_dt"])
    df["end_dt"] = pd.to_datetime(df["end_dt"])
    return df


data_sets = initDataSets()


def hhmm2mins(hhmm):
    i = int(hhmm)
    n_hrs = i // 100
    n_mins = i % 100
    return n_hrs * 60 + n_mins


def mins2hhmm(mins):
    hh = int(mins / 60)
    mm = mins - hh * 60
    return "%02d%02d" % (hh, mm)


def add2hhmm(hhmm, mins):
    return mins2hhmm(hhmm2mins(hhmm) + mins)


def lastDataBlock():
    return max(data_sets.index)


def firstDataBlock():
    return min(data_sets.index)


def setDates(sess_st, sess_end, bars_back, data_set, data_block, time_frames):
    logger.debug(
        f"sess_st={sess_st}, sess_end={sess_end}, bars_back={bars_back}, data_set={data_set}, data_block={data_block}, time_frames={time_frames}"
    )
    tf = int(time_frames[0])
    number_segments = 10

    use_daily = False
    if "1440" in time_frames:
        use_daily = True
    if "D" in time_frames:
        use_daily = True
    if not use_daily:
        bars_per_session = hhmm2mins(sess_end) - hhmm2mins(sess_st) / tf
        bars_back = math.ceil(200 / bars_per_session)

    seg_size = int(
        (data_sets.loc[data_set]["end_dt"] - data_sets.loc[data_set]["start_dt"]).days
        / number_segments
    )
    start_dt = data_sets.loc[data_set]["start_dt"] + pd.DateOffset(
        (data_block - 1) * seg_size
    )
    pre_start_dt = start_dt - pd.DateOffset(round((bars_back / 5) * 7))
    end_dt = start_dt + pd.DateOffset(seg_size)
    return {
        "pre_start_dt": pre_start_dt,
        "start_dt": start_dt,
        "end_dt": end_dt,
        "bt_start_dt": data_sets.loc[data_set]["start_dt"],
        "bt_end_dt": data_sets.loc[data_set]["end_dt"],
    }


########## proto typing
def format_chart_series(data_series):
    # 1:@CL:15:m,2:@CL:1440:m
    arr = []
    for i, ds in enumerate(data_series):
        arr.append(":".join([str(i)] + ds))
    return ",".join(arr)


Day = 0
Swing = 0
BOS = 1


def setBosBaseParams(dbh, params):
    required_params = ["poi", "natr", "fract", "filter_1", "time_segment", "lsb"]
    for p in required_params:
        if p not in params:
            params[p] = use_parameter_preset(dbh, p, "default")


def dependentParams(dbh, params, defined_parms):
    rtn_parms = set()
    for p_dict in params:
        if p_dict["name"].startswith("filter_") and len(p_dict["name"].split("_")) == 2:
            ds = p_dict["name"].split("_")[1]
            for id in extractIds(p_dict):
                q = queryEntryFilter(dbh, id)
                try:
                    for p in q.long_params.split(","):
                        new_param = p.format(dn=ds)
                        if new_param not in defined_parms:
                            rtn_parms.add(new_param)
                        # rtn_parms.add(p.format(dn=ds))
                except AttributeError:
                    pass
                try:
                    for p in q.short_params.split(","):
                        new_param = p.format(dn=ds)
                        if new_param not in defined_parms:
                            rtn_parms.add(new_param)
                        # rtn_parms.add(p.format(dn=ds))
                except AttributeError:
                    pass
    return rtn_parms


def extractIds(dict):
    if dict["input_type"] == "var":
        return [dict["value"]]
    if dict["input_type"] == "range":
        if dict["data_type"] == "double":
            st, end, step = [float(x) for x in dict["value"].split(",")]
            rtn_val = [format(x, ".2f") for x in np.arange(st, end + step, step)]
            return rtn_val
        else:
            st, end, step = [int(x) for x in dict["value"].split(",")]
            rtn_val = [int(x) for x in np.arange(st, end + step, step)]
            return rtn_val
    if dict["input_type"] == "list":
        return dict["value"].split(",")
    return []


def validateParam(param, value):
    return value


def expandParam(name, value):
    split_vals = value.split(":")
    if len(split_vals) == 3:
        value += ":N"
    input_type, value, data_type, re_optimize = value.split(":")
    return {
        "name": name,
        "input_type": input_type,
        "value": value,
        "data_type": data_type,
        "re_optimize": re_optimize,
    }


def adjust_re_optimization_param(params_arr):
    rtn_arr = []
    cnt = sum([1 for v in params_arr if v["re_optimize"] == "Y"])
    for p in params_arr:
        if p["re_optimize"] == "A":
            if cnt < 5:
                p["re_optimize"] = "Y"
            else:
                p["re_optimize"] = "No"
        if p["re_optimize"] == "Y":
            p["re_optimize"] == extractIds(p)
        rtn_arr.append(p)
    return rtn_arr


def use_parameter_preset(dbh, param, preset):
    # "natr": "range:5,60,5:int",
    def_data = queryParamDef(dbh, param)
    preset_data = queryParamPreset(dbh, preset, param)
    return f"{preset_data.input_type}:{preset_data.value}:{def_data.data_type}:{def_data.re_opt}"


def set_opt_params(dbh, trade_strategy, trade_type, data_series, params):
    """ 
    [ 
        {'name': 'time_segment',
         'input_type': 'var',
         'value': '0',
         'data_type'},
        {'name': 'poi',
         'input_type': 'list',
         'value': '1,3,5,7',
         'data_type': 'int'},
        {'name': 'natr',
         'input_type': 'range',
         'value': '5,60,5'
        }
    ]
    """
    if trade_strategy == BOS:
        setBosBaseParams(dbh, params)
    params_arr = []
    defined_parms = set()
    for name in params:
        if params[name].startswith("preset:"):
            preset = params[name].split(":")[1]
            params[name] = use_parameter_preset(dbh, name, preset)
        else:
            params[name] = validateParam(name, params[name])
        tmp_var = expandParam(name, params[name])
        params_arr.append(tmp_var)
        # params_arr.append(expandParam(name, params[name]))
        defined_parms.add(name)
    params_arr = adjust_re_optimization_param(params_arr)
    for new_param in dependentParams(dbh, params_arr, defined_parms):
        params_arr.append(
            expandParam(new_param, use_parameter_preset(dbh, new_param, "default"))
        )

    return params_arr


def add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id=None,
    data_set=None,
    data_block=None,
    template_version="prototype_v4",
    jcl_version="prototype_v3",
    **params,
):
    Day = 0
    Swing = 1
    opt_params = set_opt_params(dbh, tradeStrategy, Day, data_series, params)
    symbol = data_series[0][0]
    logger.debug(f"symbol={symbol}  data_series={data_series}")

    market_id = querySecId(dbh, symbol)

    if session_id is None:
        session_id = queryDefaultSessionId(dbh, symbol)
        logger.debug(f"lookup session for {symbol}: {session_id}")
    sess = querySession(dbh, session_id)
    session_start = sess.session_start
    session_end = sess.session_end
    logger.debug(f"session: {session_start} - {session_end}")

    if not data_set or not (
        data_set >= firstDataBlock() and data_set <= lastDataBlock()
    ):
        data_set = lastDataBlock()
    if not data_block or not (data_block > 0 and data_block < 11):
        data_block = randint(1, 10)
    day_swing = Day

    fitness_function = "TSI"
    max_bars_back = 200
    trades_per_day = 1

    chart_series = format_chart_series(data_series)
    time_frames = [x[2] for x in (x.split(":") for x in chart_series.split(","))]
    logger.debug(f"chart_series={chart_series}  time_frames={time_frames}")
    dates = setDates(
        session_start, session_end, max_bars_back, data_set, data_block, time_frames
    )

    new_rec = Prototype(
        market_id=market_id,
        market_session_id=session_id,
        template_version=template_version,
        jcl_version=jcl_version,
        data_set=data_set,
        data_block=data_block,
        symbol=symbol,
        chart_series=chart_series,
        fitness_function=fitness_function,
        max_days_back=max_bars_back,
        trades_per_day=trades_per_day,
        day_swing=day_swing,
        prestart_dt=dates["pre_start_dt"],
        start_dt=dates["start_dt"],
        end_dt=dates["end_dt"],
        bt_start_dt=dates["bt_start_dt"],
        bt_end_dt=dates["bt_end_dt"],
        status="new",
        status_state="pending",
    )
    dbh.add(new_rec)
    dbh.commit()
    dbh.flush()
    proto_id = new_rec.id

    updates = {
        "in_sample_file": f"proto_{proto_id}_is.csv",
        "out_of_sample_file": f"proto_{proto_id}_oos.csv",
    }
    dbUpdatePrototype(dbh, proto_id, updates)

    for p in opt_params:
        new_rec = PrototypeParameter(
            proto_id=proto_id,
            name=p["name"],
            input_type=p["input_type"],
            data_type=p["data_type"],
            value=p["value"],
            re_optimize=p["re_optimize"],
        )
        dbh.add(new_rec)
        dbh.commit()

    return proto_id


def add_candidate(dbh, proto_id, params):
    db_proto = queryPrototype(dbh, proto_id)
    new_cand = Candidate(
        test_id=params["Test"],
        proto_id=proto_id,
        template_version="swfa_v1",
        jcl_version="swfa_v2",
        strategy_file="",
        strategy_name="",
        status="new",
        status_state="pending",
        bt_start_dt=db_proto.bt_start_dt,
        bt_end_dt=db_proto.bt_end_dt,
    )
    dbh.add(new_cand)
    dbh.commit()

    updates = {
        "strategy_name": f"proto_{proto_id}_strat_{new_cand.id}",
        "wfa_file": f"cand_{new_cand.id}",
    }
    dbUpdateCandidate(dbh, new_cand.id, updates)

    add_candidate_settings(dbh, new_cand.id, proto_id, params)
    add_candidate_parameters(dbh, new_cand.id, proto_id, params)
    """
    opt_params = setOptimizationParam(dbh, proto_id, new_cand.id, params)
    for p in opt_params:
        new_param = CandidateParameter(
            candidate_id=new_cand.id,
            name=p["name"],
            data_type=p["data_type"],
            value=p["range"],
            input_type='range',
        )
        dbh.add(new_param)
    dbh.commit()
    """


def add_candidate_settings(dbh, cand_id, proto_id, params):
    logger.debug(f"add_candidate_settings(dbh, {cand_id}, {proto_id}, {params}):")
    proto_params = queryPrototypeParams(dbh, proto_id)
    rtn = {}
    for p in proto_params:
        if p.name in params.keys():
            value = params[p.name]
            if p.data_type == "int":
                value = int(value)
            new_rec = CandidateSetting(
                candidate_id=cand_id, name=p.name, value=value, data_type=p.data_type
            )
            dbh.add(new_rec)
        elif p.input_type == "var":
            new_rec = CandidateSetting(
                candidate_id=cand_id, name=p.name, value=p.value, data_type=p.data_type
            )
            dbh.add(new_rec)

    dbh.commit()


def step_size_adjustment(dbh, opt_params, settings):
    adj_by = 0
    cnt = 8001
    adj_by = 0
    nsteps = 0
    while cnt > 8000:
        cnt = 1
        for param_name in opt_params:
            data_dict = setOptimizationParam(
                dbh, param_name, settings[param_name], nsteps, adj_by
            )
            nsteps = max(nsteps, data_dict["num_steps"])
            cnt *= data_dict["iterations"]
        logger.debug(f"cnt={cnt} with adjustment: {adj_by}")
        if cnt > 8000:
            adj_by -= 1
    return adj_by


def add_candidate_parameters(dbh, cand_id, proto_id, settings):
    logger.debug(f"add_candidate_parameters(dbh,{cand_id},{proto_id}):")
    opt_params = [
        p.name
        for p in queryPrototypeParams(dbh, proto_id)
        if p.re_optimize == "Y" and p.name in settings.keys()
    ]

    step_adj = step_size_adjustment(dbh, opt_params, settings)
    logger.debug(f"add_candidate_parameters: opt_params={opt_params}")
    cnt = 1
    for param_name in opt_params:
        logger.debug(f"name: {param_name} ===> {settings[param_name]}")
        data_dict = setOptimizationParam(
            dbh, param_name, settings[param_name], 99, step_adj
        )
        cnt *= data_dict["iterations"]
        new_rec = CandidateParameter(
            candidate_id=cand_id,
            name=param_name,
            value=data_dict["range"],
            data_type=data_dict["data_type"],
            input_type="range",
        )
        dbh.add(new_rec)
    dbh.commit()
    dbUpdateCandidate(dbh, cand_id, {"opt_iterations": cnt})


def count_iterations(start, end, step):
    logger.debug(f"count_iterations({start}, {end}, {step}):")
    ptr = start
    cnt = 0
    while ptr <= end:
        cnt += 1
        ptr += step
    return cnt


def setOptimizationParam(dbh, param_name, value, nsteps, step_adj=0):
    logger.debug(
        f"setOptimizationParam(dbh, {param_name}, {value}, {nsteps}, {step_adj}):"
    )
    param_def = queryParamDef(dbh, param_name)
    if nsteps == 0:
        num_steps = param_def.num_steps
    else:
        num_steps = param_def.num_steps + step_adj
    step_size = param_def.step_size
    min_val = param_def.min_value
    max_val = param_def.max_value
    logger.debug(
        f"num_steps={num_steps}  step_size={step_size}  min_val={min_val}  max_val={max_val}"
    )
    if param_def.data_type == "double":
        value = float(value)
        step_size = float(step_size)
        start = round(max(float(min_val), value - (int(num_steps) * step_size)), 2)
        end = round(min(float(max_val), value + (int(num_steps) * step_size)), 2)
    else:
        value = int(value)
        step_size = int(step_size)
        start = max(int(min_val), value - (int(num_steps) * step_size))
        end = min(int(max_val), value + (int(num_steps) * step_size))

    return {
        "range": f"{start},{end},{step_size}",
        "data_type": param_def.data_type,
        "iterations": count_iterations(start, end, step_size),
        "num_steps": num_steps,
    }


"""
    iterations *= count_iterations(start, end, step_size)
        logger.debug(
            f"{p.name}:  re_optimize={p.re_optimize} ==> {dict['range']} iter={iterations}"
        )
        opt_params.append(dict)
    return opt_params
"""


if __name__ == "__main__":
    time_frames = ["15"]
    bars_back = 200
    sess_st = 800
    sess_end = 1600
    data_set = 1
    data_block = 8
    r = setDates(sess_st, sess_end, bars_back, data_set, data_block, time_frames)
    time_frames = ["15", "1440"]
    r = setDates(sess_st, sess_end, bars_back, data_set, data_block, time_frames)
    logger.debug(r)

    logger.debug(f"lastDataBlock={lastDataBlock()}")
    logger.debug(data_sets)
