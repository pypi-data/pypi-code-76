import datetime


_GPS_TIME_START = datetime.datetime(1980, 1, 6, 0, 0, 0)

# ------------------------------------------------------------------------------


def weektow_to_datetime(tow, week):

    delta = datetime.timedelta(weeks=week, seconds=tow)

    return _GPS_TIME_START + delta
