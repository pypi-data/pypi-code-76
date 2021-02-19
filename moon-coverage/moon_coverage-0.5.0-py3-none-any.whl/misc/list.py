"""Miscellaneous list toolbox module."""

from operator import indexOf


def rindex(lst, value):
    """Search the last index reference of a value in a list.

    Solution from Stackoverflow: https://stackoverflow.com/a/63834895

    """
    return len(lst) - indexOf(reversed(lst), value) - 1
