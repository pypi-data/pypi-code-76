from datetime import datetime
from inspect import getframeinfo, stack, Traceback

from models.log_model import LogModel


class LogHelper:
    CRITICAL: int = 50
    FATAL: int = CRITICAL
    ERROR: int = 40
    WARNING: int = 30
    WARN: int = WARNING
    INFO: int = 20
    DEBUG: int = 10
    NOTSET: int = 0

    def __init__(self):
        self.logs: list[LogModel] = []

    def add_log(self, logType: int, message: str) -> None:
        caller: Traceback = getframeinfo(stack()[1][0])
        log = LogModel()
        log.type_log = logType
        log.filename = caller.filename
        log.function = caller.function
        log.line_number = caller.lineno
        log.message = message
        log.creation_date = datetime.now()

        self.logs.append(log)
