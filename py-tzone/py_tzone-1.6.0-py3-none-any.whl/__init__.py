__version__ = "1.6.0"

from .tz_info import tz_info

def get_tz_details(t_zone):
    if t_zone == "" or not isinstance(t_zone,str):
        return {"error":"Invalid Timezone"}
    for tz in tz_info["data"]:
        if t_zone in tz["utc"]:
            return tz
    return None