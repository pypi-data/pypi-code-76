"""
https://circleci.com/docs/2.0/workflows/#states
"""
from enum import Enum, EnumMeta


class StatusMeta(EnumMeta):
    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class Status(str, Enum, metaclass=StatusMeta):
    pass


class ErrorStates(Status):
    NOT_RUN = "not run"
    CANCELED = "canceled"
    FAILING = "failing"
    FAILED = "failed"
    NEEDS_SETUP = "needs setup"


class RunningStates(Status):
    ON_HOLD = "on hold"
    RUNNING = "running"


class SuccessStates(Status):
    SUCCESS = "success"
