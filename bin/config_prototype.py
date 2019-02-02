import sys
from loguru import logger

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
sys.path.append("C:\\ZTS\\Dropbox\\Business\\ats\\Code\\lib")

from ats_tools import add_prototype, BOS, Day
from db_query import connectDB  # ,queryEntryFilter
import pprint

dbh = connectDB()

tradeStrategy = BOS
tradeStyle = Day
#data_series = [["@CL", "15", "m"]]
data_series = [["@CL", "60", "m"]]
#data_series = [["@ES.D", "30", "m"]]
session_id = 7
data_set = 3
data_block = 1

#proto_id = add_prototype(
#    dbh,
#    tradeStrategy,
#    tradeStyle,
#    data_series,
#    session_id,
#    data_set,
#    data_block,
#)
#pprint.pprint(proto_id)

#proto_id = add_prototype(
#    dbh,
#    tradeStrategy,
#    tradeStyle,
#    data_series,
#    session_id,
#    data_set,
#    data_block,
#    time_segment="preset:default",
#    natr="preset:default",
#    poi="preset:default",
#    filter_1="preset:default",
#    filter_1_n1="range:2,19,1:int:Y",
#    fract="range:0.6,3.0,0.15:double:Y",
#    lsb="var:1:int:N",
#)
#pprint.pprint(proto_id)

#data_series = [["@CL", "60", "m"],
#               ["@CL", "1440", "m"],]
#proto_id = add_prototype(
#    dbh,
#    tradeStrategy,
#    tradeStyle,
#    data_series,
#    session_id,
#    data_set,
#    data_block,
#    time_segment="range:0,3,1:int:N",
#    poi="range:1,8,1:int:N",
#    natr="range:5,60,5:int:A",
#    filter_1="range:1,40,1:int:N",
#    filter_1_n1="range:2,19,1:int:Y",
#    filter_2="range:30,32,1:int:N",
#    fract="range:0.6,3.0,0.15:double:Y",
#    lsb="var:1:int:N",
#)
#pprint.pprint(proto_id)

data_series  = [["@CL", "15", "m"]]
time_segment = "range:0,3,1:int:N"

logger.debug("tradeStrategy = {tradeStrategy}")
logger.debug("tradeStyle = {tradeStyle}")
logger.debug("data_series = {data_series}")
logger.debug("session_id = {session_id}")
logger.debug("data_set = {data_set}")
logger.debug("data_block = {data_block}")
logger.debug("time_segment = {time_segment}")
proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id,
    data_set,
    data_block,
    time_segment=time_segment,
)
logger.debug(proto_id)
