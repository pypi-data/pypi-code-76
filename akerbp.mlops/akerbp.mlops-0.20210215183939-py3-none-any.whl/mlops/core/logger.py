#logger.py

import logging
import os
from os.path import basename

default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
base_name='main'

class CDFLogger:
    def __init__(self, base_name):
        self.base_name=base_name
    def debug(self,log):
        print(f"{self.basename}-DEBUG-{log}")
    def info(self,log):
        print(f"{self.basename}-INFO-{log}")
    def warning(self,log):
        print(f"{self.basename}-WARNING-{log}")
    def error(self,log):
        print(f"{self.basename}-ERROR-{log}")
    def critical(self,log):
        print(f"{self.basename}-CRITICAL-{log}")


def get_logger(name=base_name, format=default_format):
    """
    Set up a stream logger
    """
    
    if not os.getenv('COGNITE_API_KEY_FUNCTIONS'): #hacky test for CDF environm.
        return CDFLogger(base_name)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    stream_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(stream_handler)
    return logger