from loguru import logger
from pathlib import Path, PureWindowsPath

ats_dir_win = Path("C:\\ZTS\Dropbox\\Business\\ats")
ats_dir = Path("/Users/szagar/ZTS/Dropbox/Business/ats")
dp_dir = Path("Data/Queue/GaProtoResults")
jcl_dir = Path("JobControl")
strat_tplt_dir = Path("Code/Templates/Strategy")
jcl_tplt_dir = Path("Code/Templates/JCL")
cand_code_dir = Path("Data/CandidateCode")
strategy_code_dir = Path("Data/StrategyCode")
jcl_code_dir = Path("Data/OptimizationApiCode")
rpt_dir = Path("/Users/szagar/ZTS/Dropbox/Business/ats/Data/Queue/WfoReports")
json_dir = Path("/Users/szagar/ZTS/Dropbox/Business/ats/Data/JsonFiles")


def warn(str):
    print(f"WARNING: {str}")


f0 = PureWindowsPath(ats_dir_win)
logger.debug(f0)

f1 = PureWindowsPath(ats_dir_win / dp_dir)
logger.debug(f1)

f2 = ats_dir / dp_dir
logger.debug(f2)
