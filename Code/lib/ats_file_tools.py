import os
from loguru import logger


def oldest_dp_file_pair(queue_dir):

    files = [fn for fn in os.listdir(queue_dir) if fn.endswith("_is.csv")]
    full_path = ["{0}/{1}".format(queue_dir, x) for x in files]
    if len(full_path) == 0:
        return None, None

    is_file = min(full_path, key=os.path.getctime)
    oos_file = is_file.replace("_is", "_oos")
    if not os.path.isfile(oos_file):
        logger.critical(f"WARN WARN: {oos_file} not found")
    return is_file, oos_file


def archive_file(archive_dir, file_name):
    dest = f"{archive_dir}/{os.path.basename(file_name)}"
    os.rename(file_name, dest)
    return dest


if __name__ == "__main__":
    print(oldest_dp_file_pair())
