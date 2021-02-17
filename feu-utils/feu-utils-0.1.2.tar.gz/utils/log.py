"""Wrapping logger common format with UTC timestamp.

This module provides a common log format with a console and file handler.
The file is a wrapping log of configurable size using `RotatingFileHandler`.

FORMAT = ('%(asctime)s.%(msecs)03dZ,[%(levelname)s],(%(threadName)-10s),'
          '%(module)s.%(funcName)s:%(lineno)d,%(message)s')

"""
import inspect
import logging
from logging.handlers import RotatingFileHandler
from os import mkdir, path
from time import gmtime

FORMAT = ('%(asctime)s.%(msecs)03dZ,[%(levelname)s],(%(threadName)-10s),'
          '%(module)s.%(funcName)s:%(lineno)d,%(message)s')


def get_logfile_name(logger: logging.Logger) -> str:
    """Returns the logger's RotatingFileHandler name."""
    for h in logger.handlers:
        if isinstance(h, RotatingFileHandler):
            return h.baseFilename
    return None


def get_caller_name(depth: int = 2,
                    mod: bool = True,
                    cls: bool =False,
                    mth: bool = False) -> str:
    """Returns the name of the calling function.

    Args:
        depth: Starting depth of stack inspection.
        mod: Include module name.
        cls: Include class name.
        mth: Include method name.
    
    Returns:
        Name (string) including module[.class][.method]

    """
    stack = inspect.stack()
    start = 0 + depth
    if len(stack) < start + 1:
        return ''
    parent_frame = stack[start][0]
    name = []
    module = inspect.getmodule(parent_frame)
    if module and mod:
        name.append(module.__name__)
    if cls and 'self' in parent_frame.f_locals:
        name.append(parent_frame.f_locals['self'].__class__.__name__)
    if mth:
        codename = parent_frame.f_code.co_name
        if codename != '<module>':
            name.append(codename)
    del parent_frame, stack
    return '.'.join(name)


def is_log_handler(logger: logging.Logger, handler: object) -> bool:
    """Returns true if the handler is found in the logger.
    
    Args:
        logger (logging.Logger)
        handler (logging handler)
    
    Returns:
        True if the handler is in the logger.

    """
    if not isinstance(logger, logging.Logger):
        return False
    found = False
    for h in logger.handlers:
        if h.name == handler.name:
            found = True
            break
    return found


def get_wrapping_logger(name: str = None,
                        filename: str = None,
                        file_size: int = 5,
                        debug: bool = False,
                        log_level: int = logging.INFO,
                        **kwargs) -> logging.Logger:
    """Sets up a wrapping logger that writes to console and optionally a file.

    Initializes logging to console, and optionally a CSV formatted file.
    CSV format: timestamp,[level],(thread),module.function:line,message
    Default logging level is INFO.
    Timestamps are UTC/GMT/Zulu.

    Args:
        name: Name of the logger (if None, uses name of calling module).
        filename: Name of the file/path if writing to a file.
        file_size: Max size of the file in megabytes, before wrapping.
        debug: enable DEBUG logging (default INFO)
        kwargs: Optional overrides for RotatingFileHandler
    
    Returns:
        A logger with console stream handler and (optional) file handler.
    """
    # FORMAT = ('%(asctime)s.%(msecs)03dZ,[%(levelname)s],(%(threadName)-10s),'
    #           '%(module)s.%(funcName)s:%(lineno)d,%(message)s')
    log_formatter = logging.Formatter(fmt=FORMAT,
                                      datefmt='%Y-%m-%dT%H:%M:%S')
    log_formatter.converter = gmtime

    if name is None:
        name = get_caller_name()
    logger = logging.getLogger(name)

    if debug or logger.getEffectiveLevel() == logging.DEBUG:
        log_lvl = logging.DEBUG
    else:
        log_lvl = log_level
    logger.setLevel(log_lvl)
    #: Set up log file
    if filename is not None:
        try:
            if filename.startswith('~'):
                filename = filename.replace('~', path.expanduser('~'))
            if not path.isdir(path.dirname(filename)):
                mkdir(path.dirname(filename))
            mode = 'a'
            max_bytes = int(file_size * 1024 * 1024)
            backup_count = 2
            encoding = None
            delay = 0
            for kw in kwargs:
                if kw == 'backupCount':
                    backup_count = kwargs[kw]
                elif kw == 'delay':
                    delay = kwargs[kw]
                elif kw == 'encoding':
                    encoding = kwargs[kw]
                elif kw == 'mode':
                    mode = kwargs[kw]
                elif kw == 'maxBytes':
                    max_bytes = kwargs[kw]
            file_handler = RotatingFileHandler(
                filename=filename,
                mode=mode,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding=encoding,
                delay=delay)
            file_handler.name = name + '_file_handler'
            file_handler.setFormatter(log_formatter)
            file_handler.setLevel(log_lvl)
            if not is_log_handler(logger, file_handler):
                logger.addHandler(file_handler)
        except Exception as e:
            logger.error('Could not create RotatingFileHandler {} ({})'
                .format(filename, e))
    #: Set up console log
    console_handler = logging.StreamHandler()
    console_handler.name = name + '_console_handler'
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(log_lvl)
    if not is_log_handler(logger, console_handler):
        logger.addHandler(console_handler)

    return logger
