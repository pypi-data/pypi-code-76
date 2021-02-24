from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone as get_tz


def getUtcDate(date):
    utc = timezone('UTC')
    tz = get_tz()  # local timezone
    local_date = tz.localize(date)
    utc_date = local_date.astimezone(utc)
    return utc_date
