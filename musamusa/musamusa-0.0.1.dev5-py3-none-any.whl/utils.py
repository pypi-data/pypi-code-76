# TODO
"""
        nikw project

        utils.py : various functions
        _______________________________________________________________________

        * add_prefix_to_strlines()
        * invertdict()
        * normpath()
"""
import os
import os.path


def add_prefix_to_strlines(_lines, _prefix):
    """
        add_prefix_to_strlines()

        Add a (str)_prefix at the beginning of a bunch of _lines.

        PARAMETERS:
            * (str)_lines : several lines separared by \n
            * (str)_prefix : the to be added prefix

        RETURNED VALUE : (str)several lines separared by \n
    """
    res = []
    for line in _lines.split("\n"):
        res.append(_prefix+line)
    return "\n".join(res)


def invertdict(src):
    """
        invertdict()

        Return the inverse of (dict)src, each key becoming a value and vice versa.
        _______________________________________________________________________

        PARAMETER: (dict)src, the dict to be inversed

        RETURNED VALUE : (dict)the reversed dictionary
    """
    return {v: k for k, v in src.items()}


def normpath(path):
    """
        normpath()

        Return a human-readable (e.g. "~" -> "/home/myhome/" on Linux systems),
        normalized version of a path.

        The returned string may be used as a parameter given to by
        os.path.exists() .
        _______________________________________________________________________

        PARAMETER : (str)path

        RETURNED VALUE : the expected string
    """
    res = os.path.normpath(os.path.abspath(os.path.expanduser(path)))

    if res == ".":
        res = os.getcwd()

    return res
