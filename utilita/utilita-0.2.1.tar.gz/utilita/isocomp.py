import isoweek
import datetime

import logging
log = logging.getLogger("[🔧utilita]")
log.addHandler(logging.NullHandler()) # ignore log messages by defualt

def is_leap_day(date):
  return date.month == 2 and date.day == 29

def is_in_leap_week(date):
  return isoweek.Week.withdate(date).week == 53

def is_in_week_prior_leap_week(date):
  same_day_next_week = date + datetime.timedelta(days=7)
  return is_in_leap_week(same_day_next_week)

def has_leap_week(year: int):
  return isoweek.Week(year, 53).week == 53

def last_year(date):
  return isoweek.Week.withdate(date).year - 1

def days_since_same_date_last_year(date):
  return 7 * 53 if is_in_leap_week(date) or has_leap_week(last_year(date)) else 7 * 52