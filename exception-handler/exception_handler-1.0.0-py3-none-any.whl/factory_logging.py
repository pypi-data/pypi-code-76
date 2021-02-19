import logging
import sys
from loguru import logger
from config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)


def init_log():
    # set loguru format for root logger
    logging.getLogger().handlers = [InterceptHandler()]

    # logging properties are defined in config.py
    _time = "<fg #ffb86c>{time:DD-MM-YYYY HH:mm:ss}</fg #ffb86c>"
    _level = "<m>{level}</m>"
    _message = "<level>{message}</level>"
    logger.add(
        sys.stdout,
        colorize=True,
        level=settings.LOG_LEVEL,
        format=f"{_time} {_level} {_message}",
        backtrace=settings.LOG_BACKTRACE,
        diagnose=settings.DIAGNOSE,
    )

    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.basicConfig(handlers=[InterceptHandler()], level=0)


def report_log_error(
        error_code,
        context_globals,
        error_exception,
        owner="",
        **kwargs,
):
    _user = f"USER|PARTNER: {owner}"
    _main_session = kwargs.get("main-session")
    _session = kwargs.get("session")
    _error_owner = f"{_user} | {_main_session} | {_session}"
    error_logger = [
        _error_owner,
        error_code.name,
        error_code.value,
        context_globals["__name__"],
        str(error_exception)
    ]
    ",".join(error_logger)
    logger.error(error_logger)
    logger.exception(error_exception)


def report_log_trace():
    ...
