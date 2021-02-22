"""Exceptions (and keywords for raising them) to be used with RPAListener."""
from robot.libraries.BuiltIn import BuiltIn
from robot.errors import ExecutionFailed
from robot.api import logger


class BusinessException(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = False


class ContinuableApplicationException(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = False


class FatalApplicationException(RuntimeError):
    ROBOT_EXIT_ON_FAILURE = False


class ExceptionRaisers:
    def raise_business_exception(self, msg):
        raise BusinessException(msg)

    def raise_application_exception(self, msg, fatal=True):
        if fatal:
            raise FatalApplicationException(msg)
        else:
            raise ContinuableApplicationException(msg)
