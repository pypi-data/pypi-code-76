from dataclasses import dataclass
from datetime import datetime, timedelta, time as time_class
from enum import IntEnum
from typing import Set, Union


class Day(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def today(cls) -> 'Day':
        today = datetime.now()
        return cls(today.weekday())

    def __sub__(self, other):
        if not isinstance(other, Day):
            raise TypeError(f'Wrong type provided, got {other}')
        return self.value - other.value


class ScheduleConfigurationError(Exception):
    pass


@dataclass
class Instant(object):
    day: Day
    time: time_class

    @classmethod
    def now(cls) -> 'Instant':
        now = datetime.now()
        day = Day(now.weekday())
        time = now.time()
        return Instant(day, time)

    def next_datetime(self) -> datetime:
        now = datetime.now()
        days_ahead = self.day - Day.today()

        is_in_the_past = days_ahead < 0 or (days_ahead == 0 and now.time() > self.time)
        if is_in_the_past:
            days_ahead += 7

        next_date = now + timedelta(days_ahead)
        future_datetime = datetime.combine(next_date.date(), self.time)
        return future_datetime


class Schedule(object):

    def __init__(self):
        self.days: Set[Day] = set()
        self.time: Union[time_class, None] = None

    def __repr__(self):
        return f'{self.__class__.__qualname__} on {self.days} at {self.time}'

    def instants(self):
        self._raise_exception_if_not_valid()
        for day in self.days:
            yield Instant(day, self.time)

    def at(self, time_string: str):
        self.time = self._time_string_to_datetime(time_string)
        return self

    @classmethod
    def _time_string_to_datetime(cls, time_string: str):
        split_string = cls._split_time_string(time_string)
        time_format = {1: '%H', 2: '%H:%M', 3: '%H:%M:%S'}
        time_format_string = time_format[len(split_string)]

        schedule_datetime = datetime.strptime(time_string, time_format_string)
        return schedule_datetime.time()

    @staticmethod
    def _split_time_string(time_string: str):
        split_string = time_string.split(':')
        if 1 < len(split_string) > 3:  # valid 1 <= x <= 3
            e = f'Invalid time string provided, {time_string}'
            raise ScheduleConfigurationError(e)
        return split_string

    def every(self, *days) -> 'Schedule':
        """
        Sets the schedule to be active on the specified days.
        @param days: the exact days when the schedule will be active
        """
        self.days = set(days)
        return self

    def every_day(self) -> 'Schedule':
        """
        Sets the schedule to be active every day of the week.
        """
        self.days = {day for day in Day}
        return self

    def exclude(self, *days) -> 'Schedule':
        """
        Excludes the specified days from the schedule.

        Example:
        >>> schedule = Schedule().between(Day.Monday, Day.FRIDAY)
        >>> schedule.exclude(Day.THURSDAY)
        >>> print(schedule)
        @param days: the days to remove from the schedule
        """
        excluded_days = set(days)
        self.days = self.days - excluded_days
        return self

    def between(self, *days) -> 'Schedule':
        """
        TODO: this might be confusing with time; consider if it should be removed.
        Sets the schedule to be active between the specified days (inclusive).
        @param days: the extremes of the interval
        """
        if len(days) != 2:
            e = f'Schedules between days require exactly two days, got {days}'
            raise ScheduleConfigurationError(e)

        start_day, end_day = days[0], days[1]
        self.days = self._weekdays_between(start_day, end_day)
        return self

    @staticmethod
    def _weekdays_between(start_day: Day, end_day: Day) -> Set[Day]:
        if start_day == end_day:  # e.g. Friday to Friday
            end_day += 6
        if start_day > end_day:  # e.g. Saturday to Tuesday
            end_day += 7

        days_interval = {Day(index % 7) for index in range(start_day, end_day + 1)}
        return days_interval

    def weekdays(self):
        """Monday to Friday"""
        self.days = {day for day in Day}
        self.exclude(Day.SATURDAY, Day.SUNDAY)
        return self

    def weekends(self):
        """Saturday and Sunday"""
        self.days = {Day.SATURDAY, Day.SUNDAY}
        return self

    def is_active_today(self) -> bool:
        """
        Returns true if the schedule is set to be active today.
        """
        self._raise_exception_if_not_valid()

        today = datetime.now()
        day = Day(today.weekday())
        return day in self.days

    def is_valid(self) -> bool:
        return len(self.days) != 0 and self.time is not None

    def _raise_exception_if_not_valid(self) -> None:
        if not self.is_valid():
            e = 'Valid schedules must specify a time and at least one day.'
            raise ScheduleConfigurationError(e)
