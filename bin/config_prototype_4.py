import sys

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
sys.path.append("C:\\ZTS\\Dropbox\\Business\\ats\\Code\\lib")

from ats_tools import add_prototype, BOS, Day
from db_query import connectDB  # ,queryEntryFilter
import pprint

dbh = connectDB()

tradeStrategy = BOS
tradeStyle = Day
template_version = "prototype_v4"
jcl_version = "prototype_v4"

## parameter syntax
#  <input_type>:<value>:<data_type>:<re_optimize>
#  input_type  : range, list, var
#  value       :
#  data_type   : int, double
#  re_optimize : Y, N

session_id = None
template_version = "prototype_v5"
jcl_version = "prototype_v4"

for tf in ["45"]:
    for sym in (
        "@BO",
        "@C",
        "@CL",
        "@EMD.D",
        "@ES.D",
        "@GC",
        "@HO",
        "@LC",
        "@LH",
        "@NG",
        "@NQ.D",
        "@QM",
        "@RB",
        "@RTY.D",
        "@S",
        "@SI",
        "@W",
        "@YM.D",
    ):
        data_series = [[sym, tf, "m"],
                       [sym, "1440", "m"],
                      ]

        print(f"data_series={data_series}")
        proto_id = add_prototype(
            dbh,
            tradeStrategy,
            tradeStyle,
            data_series,
            session_id=session_id,
            template_version=template_version,
            jcl_version=jcl_version,
            poi="preset:default",
            filter_1="preset:default",
            filter_1_n1="preset:default",
            filter_1_n2="preset:default",
            filter_2="preset:default",   #         = "var:29:int",
            # filter_2_n1      = "preset:default",
            # filter_2_n2      = "preset:default",
            natr="preset:default",
            fract="preset:default",
            lsb="preset:default",
            time_segment="preset:default",
        )
        pprint.pprint(proto_id)

exit()
