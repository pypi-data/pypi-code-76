# helpers.py
import os
from pathlib import Path

from akerbp.mlops.core import logger


logging=logger.get_logger(name='mlops_core')

def get_top_folder(s):
    if isinstance(s, str):
        return s.split(os.sep)[0]
    elif isinstance(s, Path):
        return s.parents[len(s.parents)-2]


def as_import_path(file_path):
    if file_path:
        if not isinstance(file_path, str):
            file_path=str(file_path)
        return file_path.replace(os.sep,'.').replace('.py','')
    else:
        logging.debug(f"Empty file path -> empty import path returned")
