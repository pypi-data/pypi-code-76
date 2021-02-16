import datetime
import calendar
from dateutil.relativedelta import relativedelta, TH, MO


class Holiday(datetime.datetime):
    THANKSGIVING = "thanksgiving"
    CHRISTMAS = "christmas"
    NEW_YEARS = "newyears"
    INDEPENDENCE = "independence"
    MEMORIAL = "memorial"
    LABOR = "labor"

    def __new__(cls, holiday_in):
        year = datetime.datetime.now().year
        holiday = holiday_in.lower()

        if holiday == Holiday.THANKSGIVING:
            # fourth thursday in November
            month = 11
            november = datetime.datetime(year=year, month=month, day=1)
            day = (november + relativedelta(day=31, weekday=TH(-1))).day
        elif holiday == Holiday.CHRISTMAS:
            month = 12
            day = 25
        elif holiday == Holiday.NEW_YEARS or holiday == "new years":
            month = 1
            day = 1
        elif holiday == Holiday.INDEPENDENCE:
            month = 7
            day = 4
        elif holiday == Holiday.MEMORIAL:
            month = 5
            day = 31
        elif holiday == Holiday.LABOR:
            # first monday in September
            month = 9
            november = datetime.datetime(year=year, month=month, day=1)
            day = (november + relativedelta(day=1, weekday=MO(1))).day
        else:
            raise RuntimeError("{} is not a recognised Holiday".format(holiday))
        return super().__new__(cls, year=year, month=month, day=day)


def is_weekend(dt):
    return dt.weekday() >= 5
