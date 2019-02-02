import sys

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
sys.path.append("C:\\ZTS\\Dropbox\\Business\\ats\\Code\\lib")

from ats_tools import add_prototype, BOS, Day
from db_query import connectDB  # ,queryEntryFilter
import pprint

dbh = connectDB()

tradeStrategy = BOS
tradeStyle = Day
template_version="prototype_v4"
jcl_version="prototype_v3"

## parameter syntax
#  <input_type>:<value>:<data_type>:<re_optimize>
#  input_type  : range, list, var
#  value       :
#  data_type   : int, double
#  re_optimize : Y, N

# previously tested strategies - RL 3    
# Prototype_Config_Notes.xls   proto 54 -> 4
#
'''
data_series = [["@RTY.D", "15", "m"],
               ["@RTY.D", "1440","m"]]

proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id       = 11,
    #data_set         = 1,
    data_block       = 8,
    template_version = template_version,
    jcl_version      = jcl_version,
    
    poi          = "list:1,2,3:int:N",
    natr         = "range:5,55,5:int:Y",
    fract        = "range:0.6,3.0,0.15:double:Y",
    filter_1     = "list:12,14:int:N",
    filter_2     = "var:29:int:N",
    time_segment = "range:0,3,1:int:N",
    lsb          = "var:1:int:N",
)
pprint.pprint(proto_id)
'''

'''
# previously tested strategies - RL 3    
# Prototype_Config_Notes.xls   proto 31 -> 5
#
data_series = [["@CL", "30", "m"],
               ["@CL", "1440", "m"],
              ]

proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id       = 7,
    #data_set         = 1,
    data_block       = 9,
    template_version = template_version,
    jcl_version      = jcl_version,

    poi          = "var:7:int:N",
    natr         = "range:15,60,5:int:Y",
    fract        = "range:0.6,3.0,0.15:double:Y",
    filter_1     = "list:27,28:int:N",
    filter_2     = "var:29:int:N",
    time_segment = "range:0,3,1:int:N",
    lsb          = "range:1,3,1:int:N",
)
pprint.pprint(proto_id)
'''

'''
# previously tested strategies - RL 3
# Prototype_Config_Notes.xls   proto 49 -> 6
#
data_series = [["@LH", "20", "m"],
              ]

proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id       = 6,
    #data_set         = 
    data_block       = 9,
    template_version = template_version,
    jcl_version      = jcl_version,

    poi          = "var:5:int:N",
    natr         = "range:15,45,5:int:Y",
    fract        = "range:1.2,3.0,0.15:double:Y",
    filter_1     = "list:39:int:N",
    #filter_2     = 
    time_segment = "range:0,3,1:int:N",
    lsb          = "range:1,3,1:int:N",
)
pprint.pprint(proto_id)
'''

'''
# previously tested strategies - RL 3
# Prototype_Config_Notes.xls   proto 40 -> 7
#
data_series = [["@NG", "60", "m"],
               ["@NG", "1440", "m"],
              ]

proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id       = 7,
    #data_set         =
    data_block       = 9,
    template_version = template_version,
    jcl_version      = jcl_version,

    poi          = "var:1:int:N",
    natr         = "range:45,60,5:int:Y",
    fract        = "range:1.2,3.0,0.15:double:Y",
    filter_1     = "var:31:int:N",
    filter_2     = "var:29:int:N",
    time_segment = "range:0,3,1:int:N",
    lsb          = "range:1,3,1:int:N",
)
pprint.pprint(proto_id)
'''

'''
# previously tested strategies - RL 3
# Prototype_Config_Notes.xls   proto 39 -> 8
#
data_series = [["@NG", "30", "m"],
               ["@NG", "1440", "m"],
              ]

proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id       = 7,
    #data_set         =
    data_block       = 9,
    template_version = template_version,
    jcl_version      = jcl_version,

    poi          = "var:1:int:N",
    natr         = "range:10,40,5:int:Y",
    fract        = "range:2.25,3.0,0.15:double:Y",
    filter_1     = "var:31:int:N",
    filter_2     = "var:29:int:N",
    time_segment = "range:0,3,1:int:N",
    lsb          = "range:1,3,1:int:N",
)
pprint.pprint(proto_id)
'''

'''
# previously tested strategies - RL 3
# Prototype_Config_Notes.xls   proto 97 -> 9
#
data_series = [["@RTY.D", "15", "m"],
               ["@RTY.D", "1440", "m"],
              ]

proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id       = 11,
    #data_set         =
    data_block       = 9,
    template_version = template_version,
    jcl_version      = jcl_version,

    poi          = "var:3:int:N",
    natr         = "range:25,55,5:int:Y",
    fract        = "range:0.75,1.65,0.15:double:Y",
    filter_1     = "var:5:int:N",
    filter_2     = "var:29:int:N",
    time_segment = "range:0,3,1:int:N",
    lsb          = "range:1,3,1:int:N",
)
pprint.pprint(proto_id)
'''

'''
# previously tested strategies - RL 3
# Prototype_Config_Notes.xls   proto 104 -> 10
#
data_series = [["@RTY.D", "15", "m"],
               ["@RTY.D", "1440", "m"],
              ]

proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id       = 4,
    #data_set         =
    data_block       = 9,
    template_version = template_version,
    jcl_version      = jcl_version,

    poi          = "var:7:int:N",
    natr         = "range:5,30,5:int:Y",
    fract        = "range:0.9,1.8,0.15:double:Y",
    filter_1     = "var:6:int:N",
    filter_2     = "var:29:int:N",
    time_segment = "range:0,3,1:int:N",
    lsb          = "range:1,3,1:int:N",
)
pprint.pprint(proto_id)
'''

# previously tested strategies - RL 3
# Prototype_Config_Notes.xls   proto 2 -> 11
#
data_series = [["@CL", "15", "m"],
              ]

'''
proto_id = add_prototype(
    dbh,
    tradeStrategy,
    tradeStyle,
    data_series,
    session_id       = 7,
    #data_set         =
    data_block       = 9,
    template_version = template_version,
    jcl_version      = jcl_version,

    poi          = "var:4:int:N",
    natr         = "range:5,60,5:int:Y",
    fract        = "range:1.5,2.7,0.15:double:Y",
    filter_1     = "list:21,24:int:N",
    time_segment = "range:0,3,1:int:N",
    lsb          = "range:1,3,1:int:N",
)
pprint.pprint(proto_id)
'''
