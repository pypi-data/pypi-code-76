import time
import logging

logger = logging.getLogger(__name__)

def to_struct_time(t):
    """Converts a UNIX time, a time string, or a struct_time to a struct_time.
    """

    if t is None:
        return t

    if type(t) == float:
        return time.gmtime(t)
    elif type(t) == int:
        return time.gmtime(t)
    elif type(t) == str:
        return time.strptime(t, "%Y-%m-%d %H:%M:%S")
    elif type(t) == time.struct_time:
        return t

    logger.debug("parse_time: could not parse time: ", t)
    return None

def to_unix_time(t):
    """Converts a UNIX time, a time string, or a struct_time to a UNIX time.
    """

    if t is None:
        return t

    if type(t) == float:
        return t
    elif type(t) == int:
        return float(t)
    elif type(t) == str:
        return time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))
    elif type(t) == time.struct_time:
        return time.mktime(t)

    logger.debug("parse_time: could not parse time: ", t)
    return None
