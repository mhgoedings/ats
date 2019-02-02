import datetime
from db_query import connectDB, querySession


def setSessionVars(dbh, id):
    sess = querySession(dbh, id)
    return sess.session_start, sess.session_end


def setDataSeries(series):
    # 1:@RTY.D:120:m,2:@RTY.D:1440:m
    ds = []
    for s in series.split(","):
        sn, symbol, tf, tf_unit = s.split(":")
        tf_dict = {"sn": sn, "symbol": symbol, "tf": tf, "tf_unit": tf_unit}
        ds.append(tf_dict)
    return ds


def formatDate(from_dt):
    return datetime.datetime.strftime(from_dt, "%m/%d/%Y")
