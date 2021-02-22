from datetime import datetime
from unittest import TestCase

import pytest
from freezegun import freeze_time

from symbiotic.schedule import Day, Schedule, ScheduleConfigurationError, Instant


class Test_Schedule_DayTime_Unit(TestCase):

    def test_schedule_is_valid(self):
        schedule = Schedule().every(Day.MONDAY).at('08:00')
        self.assertTrue(schedule.is_valid())

    def test_schedule_is_not_valid_missing_time(self):
        schedule = Schedule().every(Day.MONDAY)
        self.assertFalse(schedule.is_valid())

    def test_schedule_is_not_valid_missing_days(self):
        schedule = Schedule().at('07:35')
        self.assertFalse(schedule.is_valid())


class Test_Schedule_Days_Unit(TestCase):

    @freeze_time("2021-02-17")  # Wednesday
    def test_schedule_one_day(self):
        schedule = Schedule().every(Day.WEDNESDAY).at('06:15')
        self.assertTrue(schedule.is_active_today())

    def test_schedule_not_valid_missing_time(self):
        schedule = Schedule().weekends()
        self.assertFalse(schedule.is_valid())

    def test_empty_schedule(self):
        schedule = Schedule()
        with pytest.raises(ScheduleConfigurationError):
            schedule.is_active_today()

    def test_schedule_between_days_exception(self):
        schedule = Schedule()
        with pytest.raises(ScheduleConfigurationError):
            schedule.between()

    def test_schedule_between_two_days(self):
        schedule = Schedule().between(Day.TUESDAY, Day.THURSDAY)
        expected_days = {Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY}
        self.assertEqual(expected_days, schedule.days)

    def test_schedule_between_two_days_with_rollover(self):
        schedule = Schedule().between(Day.SATURDAY, Day.TUESDAY)
        expected_days = {Day.SATURDAY, Day.SUNDAY, Day.MONDAY, Day.TUESDAY}
        self.assertEqual(expected_days, schedule.days)

    def test_schedule_between_and_exclude_one_day(self):
        schedule = Schedule().between(Day.SATURDAY, Day.TUESDAY).exclude(Day.MONDAY)
        expected_days = {Day.SATURDAY, Day.SUNDAY, Day.TUESDAY}
        self.assertEqual(expected_days, schedule.days)

    def test_schedule_between_and_exclude_day_not_in_schedule(self):
        schedule = Schedule().between(Day.SATURDAY, Day.TUESDAY).exclude(Day.THURSDAY)
        expected_days = {Day.SATURDAY, Day.SUNDAY, Day.MONDAY, Day.TUESDAY}
        self.assertEqual(expected_days, schedule.days)

    def test_schedule_between_same_day(self):
        schedule = Schedule().between(Day.SATURDAY, Day.SATURDAY)
        expected_days = {Day.SATURDAY, Day.SUNDAY, Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY}
        self.assertEqual(expected_days, schedule.days)

    def test_schedule_weekdays(self):
        schedule = Schedule().weekdays()
        expected_days = {day for day in Day} - {Day.SATURDAY, Day.SUNDAY}  # all - weekend
        self.assertEqual(expected_days, schedule.days)

    def test_schedule_weekends(self):
        schedule = Schedule().weekends()
        expected_days = {Day.SATURDAY, Day.SUNDAY}  # all - weekend
        self.assertEqual(expected_days, schedule.days)


class Test_Schedule_Time_Unit(TestCase):

    def test_schedule_valid_time_hms(self):
        schedule = Schedule().at('13:15:45')
        self.assertEqual(13, schedule.time.hour)
        self.assertEqual(15, schedule.time.minute)
        self.assertEqual(45, schedule.time.second)

    def test_schedule_valid_time_hm(self):
        schedule = Schedule().at('14:55')
        self.assertEqual(14, schedule.time.hour)
        self.assertEqual(55, schedule.time.minute)

    def test_schedule_valid_time_h(self):
        schedule = Schedule().at('19')
        self.assertEqual(19, schedule.time.hour)

    @freeze_time("2021-02-19 17:58:00")  # Friday - two minutes before scheduled time
    def test_next_datetime_today(self):
        day = Day.FRIDAY
        scheduled_time = datetime(2021, 2, 19, 18, 0, 0).time()
        instant = Instant(day, scheduled_time)

        next_datetime = instant.next_datetime()
        expected_datetime = datetime(2021, 2, 19, 18, 0, 0)

        self.assertEqual(expected_datetime, next_datetime)

    @freeze_time("2021-02-19 18:00:01")  # Friday - one second after scheduled time
    def test_next_datetime_next_week(self):
        day = Day.FRIDAY
        scheduled_time = datetime(2021, 2, 19, 18, 0, 0).time()
        instant = Instant(day, scheduled_time)

        next_datetime = instant.next_datetime()
        expected_datetime = datetime(2021, 2, 26, 18, 0, 0)  # one week after

        self.assertEqual(expected_datetime, next_datetime)
