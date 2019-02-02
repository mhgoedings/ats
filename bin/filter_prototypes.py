#import pandas as pd
import sys
import os
from pathlib import Path

from loguru import logger

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
from config_vars import ats_dir
from candidate_tools import run_filter

archive_dir = f"{ats_dir}/Archive/DPfiles"
data_dir    = f"{ats_dir}/Data/Queue/GaProtoResults"
log_dir = "/Users/szagar/ZTS/Dropbox/Business/ats/Logs"

log_file = f"{log_dir}/{Path(__file__).stem}"

# For scripts
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": log_file, "serialize": False},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)

logger.debug("start run_filter")
logger.debug("archive_dir: {archive_dir}")
logger.debug("data_dir   : {data_dir}")

cnt = run_filter(data_dir,archive_dir)
logger.debug("run_filter returned {cnt} count")

