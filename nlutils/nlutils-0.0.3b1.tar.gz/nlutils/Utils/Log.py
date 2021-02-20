import time
import os
from datetime import datetime
from ..CommonDefine import LogLevel

# DIS
# from .CommonDefine import LogLevel

import logging
import coloredlogs

def get_local_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Logger(object):
    _instance = None

    @classmethod
    def get_logger(cls, level='INFO', write_to_file=False, log_path='/tmp/log-{}'.format(get_local_time())):
        if cls._instance:
            return cls._instance
        write_to_file = write_to_file
        if write_to_file:
            if not log_path:
                raise ValueError("Argument [log_path] cannot be None when write_to_file is True")
            else:
                log_path = log_path
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        # fhandler = logging.FileHandler(log_path)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        fmt = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        # fhandler.setFormatter(formatter)
        logger.addHandler(handler)
        # logger.addHandler(fhandler)
        coloredlogs.install(fmt=fmt, level=level, logger=logger)
        cls._instance = logger
        return cls._instance
    
    @staticmethod
    def log_performance(func):
        def wrapper():
            start = time.time()
            func()
            end = time.time()
            print("\033[1;36m{}\033[0m \033[1;34mPERFORMANCE: {} consumes {} seconds\033[0m".format(get_local_time(), func.__name__, end -start))
        return wrapper        

if __name__ == '__main__':
    # calculate_time()
    # Logger.get_logger().warning("This is a test warning.")
    # Logger.get_logger().error("This is a test error.")
    Logger.get_logger().debug("This is a test fatal.")
    Logger.get_logger().warn("This is a test fatal.")
    Logger.get_logger().error("This is a test fatal.")
    # Logger.get_logger().info("This is a test info.")
    # Logger.get_logger().log_debug("This is a test debug.")