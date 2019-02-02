#!C:\Users\Administrator\Anaconda3\envs\ats1\python.exe
import sys
import os
from pathlib import Path

from loguru import logger

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
sys.path.append("C:\\ZTS\\Dropbox\\Business\\ats\\Code\\lib")

from candidate_tools import run_test

## logger.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")
## logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")
## @logger.catch
## def my_function(x, y, z):
## Asynchoronous
##    logger.add("somefile.log", enqueue=True)

## For libraries
#logger.disable("my_library")
#logger.info("No matter added sinks, this message is not displayed")
#logger.enable("my_library")
#logger.info("This message however is propagated to the sinks")

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
    "extra": {"user": "someone"}
}
logger.configure(**config)
#logger.add(f"{log_dir}/file_{time}.log")

logger.debug("here")

#rtn = run_generate_code()
rtn = run_test('1725')
logger.debug(f"candidates processed: {rtn}")


