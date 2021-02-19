# helpers.py
import os
from akerbp.mlops.core import logger


logging=logger.get_logger(name='mlops_core')

def get_top_folder(s):
    return s.split(os.sep)[0]


def as_import_path(file_path):
    if file_path:
        return file_path.replace(os.sep,'.').replace('.py','')
    else:
        logging.debug(f"Empty file path -> empty import path returned")
