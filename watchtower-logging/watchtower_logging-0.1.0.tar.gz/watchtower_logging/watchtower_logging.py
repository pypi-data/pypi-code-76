import logging
import os
import types
from watchtower_logging.watchtower_handler import WatchTowerHandler
from watchtower_logging.exceptions import loggingException
from pythonjsonlogger import jsonlogger
import random
import string
import datetime
import pytz
import traceback

__version__ = '0.4.0'

DONE_LEVEL_NUM = logging.INFO + 2
START_LEVEL_NUM = logging.INFO + 1
EXECUTION_ID_LENGTH = 10
DEFAULT_FLUSH_INTERVAL = 5.0
logging.addLevelName(DONE_LEVEL_NUM, 'DONE')
logging.addLevelName(START_LEVEL_NUM, 'START')

class logLevels(object):

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    START = START_LEVEL_NUM
    DONE = DONE_LEVEL_NUM
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def logaction(self, msg, lvl_num, args, data=None, **kws):
    if self.isEnabledFor(lvl_num):
        if not data is None:
            if lvl_num >= logLevels.ERROR:
                data['traceback'] = traceback.format_exc()

            if 'extra' in kws:
                if 'data' in kws['extra']:
                    raise loggingException('Duplicate `data` key, please merge the data you are passing with the entry in `extra`.')
                else:
                    extra = kws.pop('extra')
                    extra = {'data': data, **extra}
            else:
                extra = {'data': data}
        else:
            extra = kws.pop('extra', {})

            if lvl_num >= logLevels.ERROR:
                data = {'traceback': traceback.format_exc()}
                if 'data' in extra:
                    raise loggingException('Duplicate `data` key, please merge the data you are passing with the entry in `extra`.')
                extra['data'] = data

        if not self._execution_id is None:
            extra['execution_id'] = self._execution_id

        # Yes, logger takes its '*args' as 'args'.
        self._log(lvl_num, msg, args, extra=extra, **kws)


def done(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=DONE_LEVEL_NUM, args=args, data=data, **kws)

def start(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=START_LEVEL_NUM, args=args, data=data, **kws)

def logdebug(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.DEBUG, args=args, data=data, **kws)

def info(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.INFO, args=args, data=data, **kws)

def warning(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.WARNING, args=args, data=data, **kws)

def error(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.ERROR, args=args, data=data, **kws)

def critical(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.CRITICAL, args=args, data=data, **kws)

def setExecutionId(self, execution_id=None):
    if execution_id is None:
        self._execution_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=EXECUTION_ID_LENGTH))
    else:
        self._execution_id = execution_id

class CustomJsonFormatter(jsonlogger.JsonFormatter):

    converter = datetime.datetime.utcfromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        ct = pytz.utc.localize(ct)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S%z")
            s = "%s,%03d" % (t, record.msecs)
        return s



def getLogger(beam_id, name=None, execution_id=None, token=None, host=None, protocol=None,
              level=logLevels.START, debug=False, path=None, console=False, send=True, use_threading=None):

    # create logger
    name = name or os.environ.get('FUNCTION_NAME', 'watchtower-logging')
    logger = logging.getLogger(name)
    logger.logaction = types.MethodType(logaction, logger)
    logger.done = types.MethodType(done, logger)
    logger.start = types.MethodType(start, logger)
    logger.debug = types.MethodType(logdebug, logger)
    logger.info = types.MethodType(info, logger)
    logger.warning = types.MethodType(warning, logger)
    logger.error = types.MethodType(error, logger)
    logger.critical = types.MethodType(critical, logger)
    logger.setExecutionId = types.MethodType(setExecutionId, logger)
    logger.setLevel(level)

    if send:
        if use_threading is None:
            if (not os.environ.get('GCP_PROJECT') is None) and (not os.environ.get('FUNCTION_NAME') is None):
                # Cloud Functions does not allow threading, so set to negative flush interval -> blocking calls
                flush_interval = -1.0
            else:
                flush_interval = DEFAULT_FLUSH_INTERVAL
        elif use_threading:
            flush_interval = DEFAULT_FLUSH_INTERVAL
        else:
            # set to negative flush interval -> blocking calls
            flush_interval = -1.0

        if len(logger.handlers) == 0 or not any(isinstance(handler, WatchTowerHandler) for handler in logger.handlers):

            # create watchtower handler and set level
            wh = WatchTowerHandler(beam_id=beam_id, token=token, debug=debug, host=host, protocol=protocol,
                                   version=__version__, flush_interval=flush_interval)
            wh.setLevel(level)

            # create formatter
            formatter = CustomJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                             datefmt="%Y-%m-%dT%H:%M:%S.%f%z")
            # add formatter to wh
            wh.setFormatter(formatter)

            # add wh to logger
            logger.addHandler(wh)

    if not path is None:

        if len(logger.handlers) == 0 or not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):

            fh = logging.FileHandler(path)
            fh.setLevel(level)
            f_formatter = CustomJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                                 datefmt="%Y-%m-%dT%H:%M:%S.%f%z")
            fh.setFormatter(f_formatter)
            logger.addHandler(fh)

    if console:

        if len(logger.handlers) == 0 or not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):

            ch = logging.StreamHandler()
            ch.setLevel(level)
            c_formatter = CustomJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                                 datefmt="%Y-%m-%dT%H:%M:%S.%f%z")
            ch.setFormatter(c_formatter)
            logger.addHandler(ch)

    logger.setExecutionId(execution_id=execution_id)

    return logger