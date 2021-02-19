import calendar
import datetime
from datetime import timedelta, date

from django.contrib.humanize.templatetags.humanize import naturalday

ISO_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_FORMAT = '%m/%d/%Y'
DATE_TIME_FORMAT = '%m/%d/%Y %I:%M %p'
DATE_TIME_WITH_SECONDS_FORMAT = '%m/%d/%Y %I:%M:%S %p'
REPORT_DATE_TIME_FORMAT = '%m%d%Y%I%M%p'


def now():
    """
    This function is used to get the current date and time object.

    :return: datetime:
    """
    return datetime.datetime.now()


def format_date(data_value):
    """
    This function is used to format the provided date object into a human readable format.

    :param data_value: date or datetime: Date object to be formatted
    :return: str: Human readable date format
    """

    if data_value:
        return naturalday(data_value)
    return None


def is_date_less_than_now(data_value):
    """
    This function is used to compare if the provided date object is less than the current date.
    This returns True if the provided date is less than the current date and False otherwise

    :param data_value: date: The date object to be compared to now
    :return: bool:
    """
    if to_start_of_day(data_value) < to_start_of_day(now()):
        return True
    return False


def get_current_year():
    """
    This function is used to get the current year integer representation (yyyy).

    :return: int: Current year
    """
    current_date = datetime.datetime.now()
    return current_date.year


def get_short_year():
    """
    This function is used to get the current Year, short version, without the century.

    :return: int: Return has two digits of the current year
    """
    current_date = datetime.datetime.now()
    return current_date.strftime("%y")


def current_time_milliseconds():
    """
    This function is used to get the current time in milliseconds.

    :return: long: Returns time in milliseconds
    """
    import time
    return round(time.time() * 1000)


def subtract_days(date_object, no_of_days):
    """
    Takes back the provided date a given number of days

    :param date_object: date: Date object to subject days from
    :param no_of_days: int: Number of days to be removed
    :return: date:
    """
    return date_object - timedelta(days=float(no_of_days))


def add_days(date_object, no_of_days):
    """
    Adds number of days to the provided date

    :param date_object: date: Date object to add days to
    :param no_of_days: int: Number of days to be added
    :return: date:
    """
    return date_object + timedelta(days=float(no_of_days))


def get_hours_between_dates(lower_date, higher_date):
    """
    Returns number of hours between two dates

    :param lower_date:
    :param higher_date:
    :return:
    """
    lower_date = lower_date.replace(tzinfo=None)
    higher_date = higher_date.replace(tzinfo=None)

    diff = higher_date - lower_date
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours + (minutes / 60) + (seconds / (60 * 60))


def get_days_between_dates(lower_date, higher_date):
    """
    Returns number of days between two dates

    :param lower_date:
    :param higher_date:
    :return:
    """
    lower_date = lower_date.replace(tzinfo=None)
    higher_date = higher_date.replace(tzinfo=None)

    diff = higher_date - lower_date
    return diff.days


def get_datetime_from_string(date_value, date_format=DATE_TIME_FORMAT):
    """
    This function is used to get a python date object using the provided date format.

    :param date_value:
    :param date_format:
    :return:
    """
    return datetime.datetime.strptime(date_value, date_format)


def get_html_datetime(date_object, date_format=DATE_TIME_FORMAT):
    """
    This function is used to format a date object into a format specified in the provided date format.

    :param date_object:
    :param date_format:
    :return:
    """
    if date_object:
        return date_object.strftime(date_format)
    return now().strftime(date_format)


def get_report_name_extension():
    return now().strftime(REPORT_DATE_TIME_FORMAT)


def get_week_days():
    """
    This function is used to get  a list of calendar days starting from Monday to Sunday.

    :return: list:
    """
    return list(calendar.day_name)


def get_current_week_day_number():
    """
    This function is used to get the numeric representation of the current day of the week.

    :return:
    """
    my_date = date.today()
    return my_date.weekday()


def get_billing_cycle_days():
    """
    This function is used to obtain the number of days remaining to reach the end of the week.

    :return: int: Returns the number of days
    """
    my_date = date.today()
    current_day = my_date.weekday()
    """ The maximum day index for python calendar for 0=monday , 6=sunday """
    max_days_index = 6
    return max_days_index - int(current_day)


def to_start_of_day(date_object):
    """
    This function is used to push time for the provided date object to the start of the day i.e. 00:00:00.

    :param date_object: date: Represents a date object
    :return: date: Return a date object with time pushed to the start of day
    """
    if not date_object:
        return None
    return datetime.datetime.combine(date_object, datetime.datetime.min.time())


def to_end_of_day(date_object):
    """
    This function is used to push time for the provided date object to the end of the day i.e. 11:59:59.

    :param date_object: date: Represents a date object
    :return: date: Return a date object with time pushed to the end of day
    """
    if not date_object:
        return None
    return datetime.datetime.combine(date_object, datetime.datetime.max.time())


def get_start_and_end_dayofweek(dayofweek):
    """
    This function is used to get a tuple containing the start date and end date of the week using the provided date object.

    For example;
        if a given date on wednesday is provided,
        the returned tuple will contain the start date and end date of the week the date lies in.

    :param dayofweek: date: Represents the date object on which you want to get it's start and end dates of it's week.
    :return: tuple: Containing the start and end date of the week
    """
    from datetime import datetime, timedelta
    dayofweek = dayofweek.strftime(DATE_FORMAT)
    date_object = datetime.strptime(dayofweek, DATE_FORMAT)
    start = date_object - timedelta(days=date_object.weekday())
    end = start + timedelta(days=6)
    return to_start_of_day(start), to_end_of_day(end)


def add_months(sourcedate, months):
    """
    This function is used to add a given number of months to the provided date object.

    :param sourcedate: date: The date object to which months are to be added
    :param months: int: Number of months to be added to the sourcedate
    :return: date: Date object in the future
    """
    month = sourcedate.month - 1 + int(months)
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
