import sys
from pathlib import Path

from loguru import logger

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
sys.path.append("C:\\ZTS\\Dropbox\\Business\\ats\\Code\\lib")

from prototype_tools import run_generate_code

log_dir = "/Users/szagar/ZTS/Dropbox/Business/ats/Logs"
#log_file = f"{log_dir}/{os.path.basename(__file__)}"
log_file = f"{log_dir}/{Path(__file__).stem}"
print(f"log_file = {log_file}")

config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": log_file, "serialize": False},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)


rtn = run_generate_code()
logger.debug(rtn)

