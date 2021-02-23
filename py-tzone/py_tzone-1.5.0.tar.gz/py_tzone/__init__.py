__version__ = "1.5.0"

from .tz_info import tz_info

def get_tz_details(t_zone):
    for tz in tz_info["data"]:
        if t_zone in tz["utc"]:
            return tz
    return None