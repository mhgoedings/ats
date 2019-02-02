#!C:\Users\Administrator\Anaconda3\envs\ats1\python.exe
import sys
import os
from pathlib import Path

from loguru import logger

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
sys.path.append("C:\\ZTS\\Dropbox\\Business\\ats\\Code\\lib")

from strategy_tools import (
    run_strategy_setup,
    #run_update_strategy_settings,
    #run_update_strategy_reopt_parameters,
    #run_generate_code,
)

log_dir = "/Users/szagar/ZTS/Dropbox/Business/ats/Logs"
log_file = f"{log_dir}/{os.path.basename(__file__)}"
log_file = f"{log_dir}/{Path(__file__).stem}"
logger.debug(f"log_file: {log_file}")

# For scripts
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": log_file, "serialize": False},
    ],
    "extra": {"user": "someone"},
}
logger.configure(**config)
# logger.add(f"{log_dir}/file_{time}.log")

logger.debug("run_strategy_setup")
rtn = run_strategy_setup()

logger.debug(f"strategies processed: {rtn}")
