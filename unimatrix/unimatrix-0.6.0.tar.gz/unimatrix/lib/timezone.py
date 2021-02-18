"""Provides an API for date and time related functions."""
import time


def now():
    """Return the current date and time, represented as milliseconds since the
    UNIX epoch.
    """
    return int(time.time() * 1000)
