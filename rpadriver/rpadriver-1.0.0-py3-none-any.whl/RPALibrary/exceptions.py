"""Exceptions for TOSLibrary."""
from collections import defaultdict

from tos.statuses import (
    FailStatus,
    SkipStatus
)


class BusinessException(Exception):
    """A known, non-techical error or another reason to stop running."""
    pass


class SkipProcessing(Exception):
    """A known case e.g., when input is invalid and nothing should be done aboot it.

    This is not a failure.
    """
    pass


class CannotCreateTaskObject(Exception):
    pass


class DataAlreadyProcessed(Exception):
    pass


class AbortException(Exception):
    pass


def get_status_by_exception(exception):
    """
    Get status string by exception.

    The given exception instance can be inherited from
    the known base exceptions defined here in RPALibrary.
    """
    mapping = {
        BusinessException: FailStatus.EXPECTED_FAIL,
        SkipProcessing: SkipStatus.SKIP,
    }
    return (
        mapping.get(exception.__class__) or
        mapping.get(
            exception.__class__.__bases__[0],
            FailStatus.FAIL
        )
    )
