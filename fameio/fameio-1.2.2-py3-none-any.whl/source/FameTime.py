# !/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum

import datetime as dt
import math
import re

from fameio.source.tools import log_and_raise



START_IN_REAL_TIME = '2000-01-01_00:00:00'
DATE_FORMAT = '%Y-%m-%d_%H:%M:%S'
DATE_REGEX = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}')
FAME_FIRST_DATETIME = dt.datetime.strptime(START_IN_REAL_TIME, DATE_FORMAT)


class TimeUnit(Enum):
    SECONDS = 0
    MINUTES = 1
    HOURS = 2
    DAYS = 3
    WEEKS = 4
    MONTHS = 5
    YEARS = 6


class Constants:
    STEPS_PER_SECOND = 1
    SECONDS_PER_MINUTE = 60
    MINUTES_PER_HOUR = 60
    HOURS_PER_DAY = 24
    DAYS_PER_YEAR = 365
    STEPS_PER_MINUTE = STEPS_PER_SECOND * SECONDS_PER_MINUTE
    STEPS_PER_HOUR = STEPS_PER_MINUTE * MINUTES_PER_HOUR
    STEPS_PER_DAY = STEPS_PER_HOUR * HOURS_PER_DAY
    STEPS_PER_YEAR = STEPS_PER_DAY * DAYS_PER_YEAR
    STEPS_PER_WEEK = STEPS_PER_DAY * 7
    STEPS_PER_MONTH = STEPS_PER_YEAR / 12

    steps_per_unit = {TimeUnit.SECONDS: STEPS_PER_SECOND,
                      TimeUnit.MINUTES: STEPS_PER_MINUTE,
                      TimeUnit.HOURS: STEPS_PER_HOUR,
                      TimeUnit.DAYS: STEPS_PER_DAY,
                      TimeUnit.WEEKS: STEPS_PER_WEEK,
                      TimeUnit.MONTHS: STEPS_PER_MONTH,
                      TimeUnit.YEARS: STEPS_PER_YEAR,
                      }


class FameTime:
    """Handles conversion of TimeSteps and TimeDurations into TimeStamps and vice versa"""

    @staticmethod
    def convert_datetime_to_fame_time_step(datetime_string):
        """Converts real Datetime string to FAME time step"""
        try:
            datetime = dt.datetime.strptime(datetime_string, DATE_FORMAT)
        except ValueError:
            log_and_raise("Invalid time stamp `{}`".format(datetime_string))
        years_since_start_time = datetime.year - FAME_FIRST_DATETIME.year
        beginning_of_year = dt.datetime(year=datetime.year, month=1, day=1, hour=0, minute=0, second=0)
        seconds_since_beginning_of_year = (datetime - beginning_of_year).total_seconds()
        return years_since_start_time * Constants.STEPS_PER_YEAR + seconds_since_beginning_of_year * Constants.STEPS_PER_SECOND

    @staticmethod
    def convert_fame_time_step_to_datetime(fame_time_steps):
        """Converts fame time step to Datetime string"""
        years_since_start_time = math.floor(fame_time_steps / Constants.STEPS_PER_YEAR)
        current_year = years_since_start_time + 2000
        beginning_of_year = dt.datetime(year=current_year, month=1, day=1, hour=0, minute=0, second=0)
        seconds_in_current_year = (fame_time_steps - years_since_start_time * Constants.STEPS_PER_YEAR) / Constants.STEPS_PER_SECOND
        datetime = beginning_of_year + dt.timedelta(seconds=seconds_in_current_year)
        return datetime.strftime(DATE_FORMAT)

    @staticmethod
    def convert_time_span_to_fame_time_steps(value, unit):
        """Converts value of TimeUnit.UNIT to fame time steps"""
        steps = Constants.steps_per_unit.get(unit)
        if steps:
            return steps * value
        else:
            raise Exception("TimeUnit conversion of '{}' not implemented.".format(unit))

    @staticmethod
    def is_datetime(string):
        """Returns `True` if given `string` matches Datetime string format and can be converted to FAME time step"""
        if isinstance(string, str):
            return DATE_REGEX.fullmatch(string.strip()) is not None
        return False
