import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from os import environ

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = "inforion.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, add_log_file=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(get_logger_level())
    # logger.setLevel(logging.INFO)
    #logger.setLevel(logging.DEBUG)
    # logger.addHandler(get_console_handler())
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True
    if add_log_file:
        logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger

def get_logger_level():
    key = "LOG_LEVEL"
    if(key in environ):
        if environ.get(key) in ('CRITICAL', 'FATAL'):
            return logging.CRITICAL
        elif environ.get(key) in ('ERROR'):
            return logging.ERROR
        elif environ.get(key) in ('WARNING', 'FATAL'):
            return logging.WARNING
        elif environ.get(key) in ('INFO'):
            return logging.INFO
        elif environ.get(key) in ('DEBUG'):
            return logging.DEBUG
        else:
            return logging.ERROR
    return logging.ERROR

def print_log_to_console():
    key = "LOG_TO_CONSOLE"
    if(key in environ):
        if environ.get(key).upper() in ('TRUE') :
            return True
        else:
            try : 
                res = int(environ.get(key))
                if(res == 1): return True
            except ValueError  :
                return False
    return False
