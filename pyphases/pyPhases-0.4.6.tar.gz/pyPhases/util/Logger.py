from enum import Enum
from functools import partial, wraps


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class Logger:
    verboseLevel: LogLevel = LogLevel.INFO

    @staticmethod
    def log(msg, system=None, level=LogLevel.INFO, end="\n"):
        msg = str(msg)
        if system != None:
            msg = "[" + system + "] " + msg

        if level == LogLevel.WARNING:
            msg = u"\033[33;1;4m%s\033[0m" % (msg)
        if level == LogLevel.ERROR:
            msg = u"\033[31;1;4m%s\033[0m" % (msg)

        if Logger.verboseLevel.value <= level.value:
            print(msg, end=end)


def classLogger(class_):
    def log(self, msg, level=LogLevel.INFO):
        system = type(self).__name__
        Logger.log(msg, system, level)

    def logDebug(self, msg):
        system = type(self).__name__
        Logger.log(msg, system, level=LogLevel.DEBUG)

    def logWarning(self, msg):
        system = type(self).__name__
        Logger.log(msg, system, LogLevel.WARNING)

    def logError(self, msg):
        system = type(self).__name__
        Logger.log(msg, system, LogLevel.ERROR)

    def logProgress(self, msg, current=0, max=100, level=LogLevel.INFO):
        system = type(self).__name__
        msg = "%s: %i/%i" % (msg, current, max)
        end = "\n" if current >= max else "\r"
        Logger.log(msg, system, level, end=end)

    class_.log = log
    class_.logDebug = logDebug
    class_.logWarning = logWarning
    class_.logError = logError
    class_.logProgress = logProgress
    return class_
