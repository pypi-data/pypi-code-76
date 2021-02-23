import time, calendar
from datetime import datetime, timedelta


def today():
    """ 今天 """
    return datetime.today()


def today_date():
    """ 今天的日期 """
    return today().date()


def int_time_now():
    """ 时间戳 """
    return int(time.time())


def year(dt=None):
    """ 日期所在的年份 """
    if dt and isinstance(dt, datetime):
        return [dt.year]
    else:
        return year(today())


def year_month(dt=None):
    """ 日期所在的年月 """
    if dt and isinstance(dt, datetime):
        ret_lst = year(dt)
        ret_lst.append(dt.month)
        return ret_lst
    else:
        return year_month(today())


def year_month_day(dt=None):
    """ 日期所在的年月日 """
    if dt and isinstance(dt, datetime):
        ret_lst = year_month(dt)
        ret_lst.append(dt.day)
        return ret_lst
    else:
        return year_month_day(today())


def date_str(dt=None, format='%Y-%m-%d'):
    """ 日期字符串 """
    if dt and isinstance(dt, datetime):
        return dt.strftime(format)
    else:
        return date_str(today())


def datetime_str(dt=None, format='%Y-%m-%d %H:%M:%S'):
    """ 带时间的日期字符串 """
    if dt and isinstance(dt, datetime):
        return dt.strftime(format)
    else:
        return datetime_str(today())


def additive(dt=None, days=None, minutes=None, seconds=None):
    """ 日期加减法 """
    if dt and isinstance(dt, datetime):
        if days and isinstance(days, int):
            dt += timedelta(days=days)
        if minutes and isinstance(minutes, int):
            dt += timedelta(minutes=minutes)
        if seconds and isinstance(seconds, int):
            dt += timedelta(seconds=seconds)
        return dt
    else:
        return additive(today(), days, minutes, seconds)


def first_month_day(dt=None):
    """ 日期所在月的第一天的 """
    if dt and isinstance(dt, datetime):
        return dt.replace(day=1)
    else:
        return first_month_day(today())


def month_days(dt=None):
    """ 日期所在月有多少天 """
    if dt and isinstance(dt, datetime):
        return calendar.monthrange(*year_month(dt))[1]
    else:
        return month_days(today())
