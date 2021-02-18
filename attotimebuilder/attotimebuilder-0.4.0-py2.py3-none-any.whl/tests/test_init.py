# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import unittest
import attotime

from decimal import Decimal, localcontext
from aniso8601 import compat
from aniso8601.builders import (DateTuple, DatetimeTuple,
                                DurationTuple, IntervalTuple,
                                TimeTuple, TimezoneTuple)
from aniso8601.exceptions import (DayOutOfBoundsError, HoursOutOfBoundsError,
                                  LeapSecondError, MidnightBoundsError,
                                  MinutesOutOfBoundsError,
                                  SecondsOutOfBoundsError,
                                  WeekOutOfBoundsError, YearOutOfBoundsError)
from aniso8601.utcoffset import UTCOffset
from attotimebuilder import AttoTimeBuilder

class TestAttoTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        testtuples = (({'YYYY': '2013', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       datetime.date(2013, 1, 1)),
                      ({'YYYY': '0001', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       datetime.date(1, 1, 1)),
                      ({'YYYY': '1900', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       datetime.date(1900, 1, 1)),
                      ({'YYYY': '1981', 'MM': '04', 'DD': '05', 'Www': None,
                        'D': None, 'DDD': None},
                       datetime.date(1981, 4, 5)),
                      ({'YYYY': '1981', 'MM': '04', 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       datetime.date(1981, 4, 1)),
                      ({'YYYY': '1981', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': '095'},
                       datetime.date(1981, 4, 5)),
                      ({'YYYY': '1981', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': '365'},
                       datetime.date(1981, 12, 31)),
                      ({'YYYY': '1980', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': '366'},
                       datetime.date(1980, 12, 31)),
                      #Make sure we shift in zeros
                      ({'YYYY': '1', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       datetime.date(1000, 1, 1)),
                      ({'YYYY': '12', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       datetime.date(1200, 1, 1)),
                      ({'YYYY': '123', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       datetime.date(1230, 1, 1)))

        for testtuple in testtuples:
            result = AttoTimeBuilder.build_date(**testtuple[0])
            self.assertEqual(result, testtuple[1])

        #Test weekday
        testtuples = (({'YYYY': '2004', 'MM': None, 'DD': None, 'Www': '53',
                        'D': None, 'DDD': None},
                       datetime.date(2004, 12, 27)),
                      ({'YYYY': '2009', 'MM': None, 'DD': None, 'Www': '01',
                        'D': None, 'DDD': None},
                       datetime.date(2008, 12, 29)),
                      ({'YYYY': '2010', 'MM': None, 'DD': None, 'Www': '01',
                        'D': None, 'DDD': None},
                       datetime.date(2010, 1, 4)),
                      ({'YYYY': '2009', 'MM': None, 'DD': None, 'Www': '53',
                        'D': None, 'DDD': None},
                       datetime.date(2009, 12, 28)),
                      ({'YYYY': '2009', 'MM': None, 'DD': None, 'Www': '01',
                        'D': '1', 'DDD': None},
                       datetime.date(2008, 12, 29)),
                      ({'YYYY': '2009', 'MM': None, 'DD': None, 'Www': '53',
                        'D': '7', 'DDD': None},
                       datetime.date(2010, 1, 3)),
                      ({'YYYY': '2010', 'MM': None, 'DD': None, 'Www': '01',
                        'D': '1', 'DDD': None},
                       datetime.date(2010, 1, 4)),
                      ({'YYYY': '2004', 'MM': None, 'DD': None, 'Www': '53',
                        'D': '6', 'DDD': None},
                       datetime.date(2005, 1, 1)))

        for testtuple in testtuples:
            result = AttoTimeBuilder.build_date(**testtuple[0])
            self.assertEqual(result, testtuple[1])

    def test_build_date_bounds_checking(self):
        #0 isn't a valid week number
        with self.assertRaises(WeekOutOfBoundsError):
            AttoTimeBuilder.build_date(YYYY='2003', Www='00')

        #Week must not be larger than 53
        with self.assertRaises(WeekOutOfBoundsError):
            AttoTimeBuilder.build_date(YYYY='2004', Www='54')

        #0 isn't a valid day number
        with self.assertRaises(DayOutOfBoundsError):
            AttoTimeBuilder.build_date(YYYY='2001', Www='02', D='0')

        #Day must not be larger than 7
        with self.assertRaises(DayOutOfBoundsError):
            AttoTimeBuilder.build_date(YYYY='2001', Www='02', D='8')

        #0 isn't a valid year for a Python builder
        with self.assertRaises(YearOutOfBoundsError):
            AttoTimeBuilder.build_date(YYYY='0000')

        with self.assertRaises(DayOutOfBoundsError):
            AttoTimeBuilder.build_date(YYYY='1981', DDD='000')

        #Day 366 is only valid on a leap year
        with self.assertRaises(DayOutOfBoundsError):
            AttoTimeBuilder.build_date(YYYY='1981', DDD='366')

        #Day must me 365, or 366, not larger
        with self.assertRaises(DayOutOfBoundsError):
            AttoTimeBuilder.build_date(YYYY='1981', DDD='367')

    def test_build_time(self):
        testtuples = (({}, attotime.attotime()),
                      ({'hh': '12.5'},
                       attotime.attotime(hour=12, minute=30)),
                      ({'hh': '23.99999999997'},
                       attotime.attotime(hour=23, minute=59, second=59,
                                         microsecond=999999, nanosecond=892)),
                      ({'hh': '1', 'mm': '23'},
                       attotime.attotime(hour=1, minute=23)),
                      ({'hh': '1', 'mm': '23.4567'},
                       attotime.attotime(hour=1, minute=23, second=27,
                                         microsecond=402000)),
                      ({'hh': '14', 'mm': '43.999999997'},
                       attotime.attotime(hour=14, minute=43, second=59,
                                         microsecond=999999, nanosecond=820)),
                      ({'hh': '1', 'mm': '23', 'ss': '45'},
                       attotime.attotime(hour=1, minute=23, second=45)),
                      ({'hh': '23', 'mm': '21', 'ss': '28.512400'},
                       attotime.attotime(hour=23, minute=21, second=28,
                                         microsecond=512400)),
                      ({'hh': '14', 'mm': '43', 'ss': '59.9999997'},
                       attotime.attotime(hour=14, minute=43, second=59,
                                         microsecond=999999, nanosecond=700)),
                      ({'hh': '24'}, attotime.attotime(hour=0)),
                      ({'hh': '24', 'mm': '00'}, attotime.attotime(hour=0)),
                      ({'hh': '24', 'mm': '00', 'ss': '00'},
                       attotime.attotime(hour=0)),
                      ({'tz': TimezoneTuple(False, None, '00', '00', 'UTC')},
                       attotime.attotime(tzinfo=UTCOffset(name='UTC',
                                                          minutes=0))),
                      ({'hh': '23', 'mm': '21', 'ss': '28.512400',
                        'tz': TimezoneTuple(False, None, '00', '00', '+00:00')},
                       attotime.attotime(hour=23, minute=21, second=28,
                                         microsecond=512400,
                                         tzinfo=UTCOffset(name='+00:00',
                                                          minutes=0))),
                      ({'hh': '1', 'mm': '23',
                        'tz': TimezoneTuple(False, None, '01', '00', '+1')},
                       attotime.attotime(hour=1, minute=23,
                                         tzinfo=UTCOffset(name='+1',
                                                          minutes=60))),
                      ({'hh': '1', 'mm': '23.4567',
                        'tz': TimezoneTuple(True, None, '01', '00', '-1')},
                       attotime.attotime(hour=1, minute=23, second=27,
                                         microsecond=402000,
                                         tzinfo=UTCOffset(name='-1',
                                                          minutes=-60))),
                      ({'hh': '23', 'mm': '21', 'ss': '28.512400',
                        'tz': TimezoneTuple(False, None, '01', '30', '+1:30')},
                       attotime.attotime(hour=23, minute=21, second=28,
                                         microsecond=512400,
                                         tzinfo=UTCOffset(name='+1:30',
                                                          minutes=90))),
                      ({'hh': '23', 'mm': '21', 'ss': '28.512400',
                        'tz': TimezoneTuple(False, None, '11', '15', '+11:15')},
                       attotime.attotime(hour=23, minute=21, second=28,
                                         microsecond=512400,
                                         tzinfo=UTCOffset(name='+11:15',
                                                          minutes=675))),
                      ({'hh': '23', 'mm': '21', 'ss': '28.512400',
                        'tz': TimezoneTuple(False, None, '12', '34', '+12:34')},
                       attotime.attotime(hour=23, minute=21, second=28,
                                         microsecond=512400,
                                         tzinfo=UTCOffset(name='+12:34',
                                                          minutes=754))),
                      ({'hh': '23', 'mm': '21', 'ss': '28.512400',
                        'tz': TimezoneTuple(False, None, '00', '00', 'UTC')},
                       attotime.attotime(hour=23, minute=21, second=28,
                                         microsecond=512400,
                                         tzinfo=UTCOffset(name='UTC',
                                                          minutes=0))),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      #https://bitbucket.org/nielsenb/aniso8601/issues/21/sub-microsecond-precision-is-lost-when
                      ({'hh': '14.9999999999999999'},
                       attotime.attotime(hour=14, minute=59, second=59,
                                         microsecond=999999,
                                         nanosecond=Decimal('999.99964'))),
                      ({'mm': '0.00000000999'},
                       attotime.attotime(nanosecond=Decimal('599.4'))),
                      ({'mm': '0.0000000999'},
                       attotime.attotime(microsecond=5, nanosecond=994)),
                      ({'ss': '0.0000001'},
                       attotime.attotime(nanosecond=100)),
                      ({'ss': '2.0000048'},
                       attotime.attotime(second=2,
                                         microsecond=4, nanosecond=800)))

        for testtuple in testtuples:
            result = AttoTimeBuilder.build_time(**testtuple[0])
            self.assertEqual(result, testtuple[1])

    def test_build_time_bounds_checking(self):
        #Leap seconds not supported
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        #https://bitbucket.org/nielsenb/aniso8601/issues/13/parsing-of-leap-second-gives-wildly
        with self.assertRaises(LeapSecondError):
            AttoTimeBuilder.build_time(hh='23', mm='59', ss='60')

        with self.assertRaises(LeapSecondError):
            AttoTimeBuilder.build_time(hh='23', mm='59', ss='60',
                                         tz=UTCOffset(name='UTC', minutes=0))

        with self.assertRaises(SecondsOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='00', mm='00', ss='60')

        with self.assertRaises(SecondsOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='00', mm='00', ss='60',
                                         tz=UTCOffset(name='UTC', minutes=0))

        with self.assertRaises(SecondsOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='00', mm='00', ss='61')

        with self.assertRaises(SecondsOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='00', mm='00', ss='61',
                                         tz=UTCOffset(name='UTC', minutes=0))

        with self.assertRaises(MinutesOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='00', mm='61')

        with self.assertRaises(MinutesOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='00', mm='61',
                                         tz=UTCOffset(name='UTC', minutes=0))

        with self.assertRaises(MinutesOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='00', mm='60')

        with self.assertRaises(MinutesOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='00', mm='60.1')

        with self.assertRaises(HoursOutOfBoundsError):
            AttoTimeBuilder.build_time(hh='25')

        #Hour 24 can only represent midnight
        with self.assertRaises(MidnightBoundsError):
            AttoTimeBuilder.build_time(hh='24', mm='00', ss='01')

        with self.assertRaises(MidnightBoundsError):
            AttoTimeBuilder.build_time(hh='24', mm='00.1')

        with self.assertRaises(MidnightBoundsError):
            AttoTimeBuilder.build_time(hh='24', mm='01')

        with self.assertRaises(MidnightBoundsError):
            AttoTimeBuilder.build_time(hh='24.1')

    def test_build_datetime(self):
        testtuples = (((DateTuple('1234', '2', '3', None, None, None),
                        TimeTuple('23', '21', '28.512400', None)),
                       attotime.attodatetime(1234, 2, 3, 23, 21, 28, 512400)),
                      ((DateTuple('1234', '2', '3', None, None, None),
                        TimeTuple('23', '21', '59.9999997', None)),
                       attotime.attodatetime(1234, 2, 3, 23, 21, 59, 999999,
                                             700)),
                      ((DateTuple('1981', '4', '5', None, None, None),
                        TimeTuple('23', '21', '59.000000000000000001', None)),
                       attotime.attodatetime(1981, 4, 5, 23, 21, 59, 0,
                                             Decimal('0.000000001'))),
                      ((DateTuple('2006', '11', '23', None, None, None),
                        TimeTuple('01', '02', '03.999999999999999999', None)),
                       attotime.attodatetime(2006, 11, 23, 1, 2, 3, 999999,
                                             Decimal('999.999999999'))),
                      #Make sure we don't truncate
                      ((DateTuple('1970', '01', '01', None, None, None),
                        TimeTuple('00', '00', '00.0000000000000000011', None)),
                       attotime.attodatetime(1970, 1, 1, 0, 0, 0, 0,
                                             Decimal('0.0000000011'))),
                      ((DateTuple('1970', '01', '01', None, None, None),
                        TimeTuple('00', '00', '09.0000000000000000099', None)),
                       attotime.attodatetime(1970, 1, 1, 0, 0, 9, 0,
                                             Decimal('0.0000000099'))),
                      ((DateTuple('1970', '01', '01', None, None, None),
                        TimeTuple('00', '09.0000000000000000099', '00', None)),
                       attotime.attodatetime(1970, 1, 1, 0, 9, 0, 0,
                                             Decimal('0.000000594'))),
                      ((DateTuple('1970', '01', '01', None, None, None),
                        TimeTuple('09.0000000000000000099', '00', '00', None)),
                       attotime.attodatetime(1970, 1, 1, 9, 0, 0, 0,
                                             Decimal('0.00003564'))))

        for testtuple in testtuples:
            result = AttoTimeBuilder.build_datetime(*testtuple[0])
            self.assertEqual(result, testtuple[1])

    def test_build_datetime_timezone(self):
        result = AttoTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                          None, None, None),
                                                TimeTuple('23', '21', '28.512400',
                                                          TimezoneTuple(False, None, '11',
                                                                        '15', '+11:15')))
        self.assertEqual(result, attotime.attodatetime(1981, 4, 5,
                                                       hour=23,
                                                       minute=21,
                                                       second=28,
                                                       microsecond=512400,
                                                       tzinfo=
                                                       UTCOffset(name='+11:15',
                                                                 minutes=675)))

    def test_build_datetime_bounds_checking(self):
        #Leap seconds not supported
        with self.assertRaises(LeapSecondError):
            AttoTimeBuilder.build_datetime(DateTuple('2016', '12', '31',
                                                     None, None, None),
                                           TimeTuple('23', '59', '60', None))

        with self.assertRaises(SecondsOutOfBoundsError):
            AttoTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                     None, None, None),
                                           TimeTuple('00', '00', '60', None))

        with self.assertRaises(SecondsOutOfBoundsError):
            AttoTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                     None, None, None),
                                           TimeTuple('00', '00', '61', None))

        with self.assertRaises(SecondsOutOfBoundsError):
            AttoTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                     None, None, None),
                                           TimeTuple('00', '59', '61', None))

        with self.assertRaises(MinutesOutOfBoundsError):
            AttoTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                     None, None, None),
                                           TimeTuple('00', '61', None, None))

    def test_build_duration(self):
        testtuples = (({'PnY': '1', 'PnM': '2', 'PnD': '3',
                        'TnH': '4', 'TnM': '54', 'TnS': '6'},
                       attotime.attotimedelta(days=428, hours=4, minutes=54,
                                              seconds=6)),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3',
                        'TnH': '4', 'TnM': '54', 'TnS': '6.5'},
                       attotime.attotimedelta(days=428, hours=4, minutes=54,
                                              seconds=6, milliseconds=500)),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3'},
                       attotime.attotimedelta(days=428)),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3.5'},
                       attotime.attotimedelta(days=428, hours=12)),
                      ({'TnH': '4', 'TnM': '54', 'TnS': '6.5'},
                       attotime.attotimedelta(hours=4, minutes=54,
                                              seconds=6, milliseconds=500)),
                      ({'TnS': '0.0000001'},
                       attotime.attotimedelta(nanoseconds=100)),
                      ({'TnS': '2.0000048'},
                       attotime.attotimedelta(seconds=2,
                                              microseconds=4, nanoseconds=800)),
                      ({'TnS': '0.000000000000000001'},
                       attotime.attotimedelta(nanoseconds=Decimal('0.000000001'))),
                      ({'PnY': '1'},
                       attotime.attotimedelta(days=365)),
                      ({'PnY': '1.5'},
                       attotime.attotimedelta(days=547, hours=12)),
                      ({'PnM': '1'},
                       attotime.attotimedelta(days=30)),
                      ({'PnM': '1.5'},
                       attotime.attotimedelta(days=45)),
                      ({'PnW': '1'},
                       attotime.attotimedelta(days=7)),
                      ({'PnW': '1.5'},
                       attotime.attotimedelta(days=10, hours=12)),
                      ({'PnD': '1'},
                       attotime.attotimedelta(days=1)),
                      ({'PnD': '1.5'},
                       attotime.attotimedelta(days=1, hours=12)),
                      ({'PnY': '0003', 'PnM': '06', 'PnD': '04',
                        'TnH': '12', 'TnM': '30', 'TnS': '05'},
                       attotime.attotimedelta(days=1279, hours=12, minutes=30,
                                              seconds=5)),
                      ({'PnY': '0003', 'PnM': '06', 'PnD': '04',
                        'TnH': '12', 'TnM': '30', 'TnS': '05.5'},
                       attotime.attotimedelta(days=1279, hours=12, minutes=30,
                                              seconds=5, milliseconds=500)),
                      #Make sure we don't truncate
                      ({'PnY': '1999.99999999999999'},
                       attotime.attotimedelta(days=729999, seconds=86399,
                                              microseconds=999999,
                                              nanoseconds=Decimal('684.64'))),
                      ({'PnM': '1.99999999999999'},
                       attotime.attotimedelta(days=59, hours=23,
                                              minutes=59, seconds=59,
                                              microseconds=999999,
                                              nanoseconds=Decimal('974.08'))),
                      ({'PnW': '1.99999999999999'},
                       attotime.attotimedelta(days=13, hours=23,
                                              minutes=59, seconds=59,
                                              microseconds=999999,
                                              nanoseconds=Decimal('993.952'))),
                      ({'PnD': '1.99999999999999'},
                       attotime.attotimedelta(days=1, hours=23,
                                              minutes=59, seconds=59,
                                              microseconds=999999,
                                              nanoseconds=Decimal('999.136'))),
                      ({'TnH': '0.0000000000000000099'},
                       attotime.attotimedelta(nanoseconds=Decimal('0.00003564'))),
                      ({'TnM': '0.0000000000000000099'},
                       attotime.attotimedelta(nanoseconds=Decimal('0.000000594'))),
                      ({'TnS': '0.0000000000000000011'},
                       attotime.attotimedelta(nanoseconds=Decimal('0.0000000011'))),
                      ({'TnS': '0.0000000000000000099'},
                       attotime.attotimedelta(nanoseconds=Decimal('0.0000000099'))))

        for testtuple in testtuples:
            result = AttoTimeBuilder.build_duration(**testtuple[0])
            self.assertEqual(result, testtuple[1])

    def test_build_interval(self):
        testtuples = (({'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None)),
                        'duration': DurationTuple(None, '1', None, None,
                                                  None, None, None)},
                       attotime.attodatetime(1981, 4, 5, hour=1, minute=1, second=0),
                       attotime.attodatetime(1981, 3, 6, hour=1, minute=1, second=0)),
                      ({'end': DateTuple('1981', '04', '05', None, None, None),
                        'duration': DurationTuple(None, '1', None, None,
                                                  None, None, None)},
                       datetime.date(1981, 4, 5),
                       datetime.date(1981, 3, 6)),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple('1.5', None, None, None,
                                                  None, None, None)},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2016, 9, 4, hour=12)),
                      ({'end': DateTuple('2014', '11', '12', None, None, None),
                        'duration': DurationTuple(None, None, None, None,
                                                  '1', None, None)},
                       datetime.date(2014, 11, 12),
                       attotime.attodatetime(2014, 11, 11, hour=23)),
                      ({'end': DateTuple('2014', '11', '12', None, None, None),
                        'duration': DurationTuple(None, None, None, None,
                                                  '4', '54', '6.5')},
                       datetime.date(2014, 11, 12),
                       attotime.attodatetime(2014, 11, 11,
                                             hour=19, minute=5,
                                             second=53, microsecond=500000)),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000001')},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2018, 3, 5,
                                             hour=23, minute=59,
                                             second=59, microsecond=999999,
                                             nanosecond=900)),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000048')},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2018, 3, 5,
                                             hour=23, minute=59,
                                             second=57, microsecond=999995,
                                             nanosecond=200)),
                      #Make sure we don't truncate
                      ({'end': DateTuple('2000', '01', '01',
                                         None, None, None),
                        'duration': DurationTuple('1999.99999999999999', None, None,
                                                  None, None, None,
                                                  None)},
                       datetime.date(year=2000, month=1, day=1),
                       attotime.attodatetime(year=1, month=4, day=30,
                                             hour=0, minute=0, second=0,
                                             microsecond=0,
                                             nanosecond=Decimal('315.36'))),
                      ({'end': DateTuple('1989', '03', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, '1.99999999999999', None,
                                                  None, None, None,
                                                  None)},
                       datetime.date(year=1989, month=3, day=1),
                       attotime.attodatetime(year=1988, month=12, day=31,
                                             hour=0, minute=0, second=0,
                                             microsecond=0,
                                             nanosecond=Decimal('25.92'))),
                      ({'end': DateTuple('1989', '03', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, '1.9999999999999',
                                                  None, None, None,
                                                  None)},
                       datetime.date(year=1989, month=3, day=1),
                       attotime.attodatetime(year=1989, month=2, day=15,
                                             hour=0, minute=0, second=0,
                                             microsecond=0,
                                             nanosecond=Decimal('60.48'))),
                      ({'end': DateTuple('1989', '03', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  '1.999999999999', None, None,
                                                  None)},
                       datetime.date(year=1989, month=3, day=1),
                       attotime.attodatetime(year=1989, month=2, day=27,
                                             hour=0, minute=0, second=0,
                                             microsecond=0,
                                             nanosecond=Decimal('86.4'))),
                      ({'end': DateTuple('2001', '01', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '14.99999999999', None,
                                                  None)},
                       datetime.date(year=2001, month=1, day=1),
                       attotime.attodatetime(year=2000, month=12, day=31,
                                             hour=9, minute=0, second=0,
                                             microsecond=0,
                                             nanosecond=36)),
                      ({'end': DateTuple('2001', '01', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, '0.00000000999',
                                                  None)},
                       datetime.date(year=2001, month=1, day=1),
                       attotime.attodatetime(year=2000, month=12, day=31,
                                             hour=23, minute=59, second=59,
                                             microsecond=999999,
                                             nanosecond=Decimal('400.6'))),
                      ({'end': DateTuple('2001', '01', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, '0.0000000999',
                                                  None)},
                       datetime.date(year=2001, month=1, day=1),
                       attotime.attodatetime(year=2000, month=12, day=31,
                                             hour=23, minute=59, second=59,
                                             microsecond=999994,
                                             nanosecond=6)),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000000000000000001')},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2018, 3, 5,
                                             hour=23, minute=59,
                                             second=59, microsecond=999999,
                                             nanosecond=Decimal('999.9999999999'))),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000000000000000009')},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2018, 3, 5,
                                             hour=23, minute=59,
                                             second=57, microsecond=999999,
                                             nanosecond=Decimal('999.9999999991'))),
                      ({'start': DatetimeTuple(DateTuple('1981', '04', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00', None)),
                        'duration': DurationTuple(None, '1', None,
                                                  '1', None, '1', None)},
                       attotime.attodatetime(1981, 4, 5, hour=1, minute=1),
                       attotime.attodatetime(1981, 5, 6, hour=1, minute=2)),
                      ({'start': DateTuple('1981', '04', '05',
                                           None, None, None),
                        'duration': DurationTuple(None, '1', None,
                                                  '1', None, None, None)},
                       datetime.date(1981, 4, 5),
                       datetime.date(1981, 5, 6)),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, '2.5', None,
                                                  None, None, None, None)},
                       datetime.date(2018, 3, 6),
                       datetime.date(2018, 5, 20)),
                      ({'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '1', None, None)},
                       datetime.date(2014, 11, 12),
                       attotime.attodatetime(2014, 11, 12, hour=1)),
                      ({'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '4', '54', '6.5')},
                       datetime.date(2014, 11, 12),
                       attotime.attodatetime(2014, 11, 12,
                                             hour=4, minute=54,
                                             second=6, microsecond=500000)),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000001')},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2018, 3, 6, nanosecond=100)),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000048')},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2018, 3, 6,
                                             second=2, microsecond=4,
                                             nanosecond=800)),
                      #Make sure we don't truncate
                      ({'start': DateTuple('0001', '01', '01',
                                           None, None, None),
                        'duration': DurationTuple('1999.99999999999999', None, None,
                                                  None, None, None,
                                                  None)},
                       datetime.date(year=1, month=1, day=1),
                       attotime.attodatetime(year=1999, month=9, day=3,
                                             hour=23, minute=59, second=59,
                                             microsecond=999999,
                                             nanosecond=Decimal('684.64'))),
                      ({'start': DateTuple('1989', '03', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, '1.99999999999999', None,
                                                  None, None, None,
                                                  None)},
                       datetime.date(year=1989, month=3, day=1),
                       attotime.attodatetime(year=1989, month=4, day=29,
                                             hour=23, minute=59, second=59,
                                             microsecond=999999,
                                             nanosecond=Decimal('974.08'))),
                      ({'start': DateTuple('1989', '03', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, '1.9999999999999',
                                                  None, None, None,
                                                  None)},
                       datetime.date(year=1989, month=3, day=1),
                       attotime.attodatetime(year=1989, month=3, day=14,
                                             hour=23, minute=59, second=59,
                                             microsecond=999999,
                                             nanosecond=Decimal('939.52'))),
                      ({'start': DateTuple('1989', '03', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  '1.999999999999', None, None,
                                                  None)},
                       datetime.date(year=1989, month=3, day=1),
                       attotime.attodatetime(year=1989, month=3, day=2,
                                             hour=23, minute=59, second=59,
                                             microsecond=999999,
                                             nanosecond=Decimal('913.6'))),
                      ({'start': DateTuple('2001', '01', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '14.99999999999', None,
                                                  None)},
                       datetime.date(year=2001, month=1, day=1),
                       attotime.attodatetime(year=2001, month=1, day=1,
                                             hour=14, minute=59, second=59,
                                             microsecond=999999,
                                             nanosecond=964)),
                      ({'start': DateTuple('2001', '01', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, '0.00000000999',
                                                  None)},
                       datetime.date(year=2001, month=1, day=1),
                       attotime.attodatetime(year=2001, month=1, day=1,
                                             hour=0, minute=0, second=0,
                                             microsecond=0,
                                             nanosecond=Decimal('599.4'))),
                      ({'start': DateTuple('2001', '01', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, '0.0000000999',
                                                  None)},
                       datetime.date(year=2001, month=1, day=1),
                       attotime.attodatetime(year=2001, month=1, day=1,
                                             hour=0, minute=0, second=0,
                                             microsecond=5,
                                             nanosecond=994)),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000000000000000001')},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2018, 3, 6,
                                             nanosecond=
                                             Decimal('0.0000000001'))),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000000000000000009')},
                       datetime.date(2018, 3, 6),
                       attotime.attodatetime(2018, 3, 6,
                                             second=2,
                                             nanosecond=
                                             Decimal('0.0000000009'))),
                      ({'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))},
                       attotime.attodatetime(1980, 3, 5, hour=1, minute=1),
                       attotime.attodatetime(1981, 4, 5, hour=1, minute=1)),
                      ({'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DateTuple('1981', '04', '05',
                                         None, None, None)},
                       attotime.attodatetime(1980, 3, 5, hour=1, minute=1),
                       datetime.date(1981, 4, 5)),
                      ({'start': DateTuple('1980', '03', '05',
                                           None, None, None),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))},
                       datetime.date(1980, 3, 5),
                       attotime.attodatetime(1981, 4, 5, hour=1, minute=1)),
                      ({'start': DateTuple('1980', '03', '05',
                                           None, None, None),
                        'end': DateTuple('1981', '04', '05',
                                         None, None, None)},
                       datetime.date(1980, 3, 5),
                       datetime.date(1981, 4, 5)),
                      ({'start': DateTuple('1981', '04', '05',
                                           None, None, None),
                        'end': DateTuple('1980', '03', '05',
                                         None, None, None)},
                       datetime.date(1981, 4, 5),
                       datetime.date(1980, 3, 5)),
                      ({'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00.0000001',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('14', '43', '59.9999997',
                                                       None))},
                       attotime.attodatetime(1980, 3, 5,
                                             hour=1, minute=1,
                                             nanosecond=100),
                       attotime.attodatetime(1981, 4, 5,
                                             hour=14, minute=43,
                                             second=59, microsecond=999999,
                                             nanosecond=700)),
                      #Test concise representation
                      ({'start': DateTuple('2020', '01', '01',
                                           None, None, None),
                        'end': DateTuple(None, None, '02',
                                         None, None, None)},
                        datetime.date(year=2020, month=1, day=1),
                        datetime.date(year=2020, month=1, day=2)),
                      ({'start': DateTuple('2008', '02', '15',
                                           None, None, None),
                        'end': DateTuple(None, '03', '14',
                                         None, None, None)},
                        datetime.date(year=2008, month=2, day=15),
                        datetime.date(year=2008, month=3, day=14)),
                      ({'start': DatetimeTuple(DateTuple('2007', '12', '14',
                                                         None, None, None),
                                               TimeTuple('13', '30', None,
                                                         None)),
                        'end': TimeTuple('15', '30', None,
                                         None)},
                        attotime.attodatetime(2007, 12, 14,
                                              hour=13, minute=30),
                        attotime.attodatetime(2007, 12, 14,
                                              hour=15, minute=30)),
                      ({'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         None)),
                        'end': DatetimeTuple(DateTuple(None, None, '15',
                                                       None, None, None),
                                             TimeTuple('17', '00', None,
                                                       None))},
                        attotime.attodatetime(2007, 11, 13,
                                              hour=9),
                        attotime.attodatetime(2007, 11, 15,
                                              hour=17)),
                      ({'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('00', '00', None,
                                                         None)),
                        'end': DatetimeTuple(DateTuple(None, None, '16',
                                                       None, None, None),
                                             TimeTuple('00', '00', None,
                                                       None))},
                        attotime.attodatetime(2007, 11, 13),
                        attotime.attodatetime(2007, 11, 16)),
                      ({'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         TimezoneTuple(False,
                                                                       True,
                                                                       None,
                                                                       None,
                                                                       'Z'))),
                        'end': DatetimeTuple(DateTuple(None, None, '15',
                                                       None, None, None),
                                             TimeTuple('17', '00', None,
                                                       None))},
                       attotime.attodatetime(2007, 11, 13,
                                             hour=9,
                                             tzinfo=UTCOffset(name='UTC',
                                                              minutes=0)),
                       attotime.attodatetime(2007, 11, 15,
                                             hour=17,
                                             tzinfo=UTCOffset(name='UTC',
                                                              minutes=0))),
                      ({'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         None)),
                        'end': TimeTuple('12', '34.567', None,
                                         None)},
                       attotime.attodatetime(2007, 11, 13,
                                             hour=9),
                       attotime.attodatetime(2007, 11, 13,
                                             hour=12, minute=34, second=34,
                                             microsecond=20000)),
                      ({'start': DateTuple('2007', '11', '13',
                                           None, None, None),
                        'end': TimeTuple('12', '34', None,
                                         None)},
                        datetime.date(year=2007, month=11, day=13),
                        attotime.attodatetime(2007, 11, 13,
                                              hour=12, minute=34)),
                      #Make sure we don't truncate
                      ({'start': DatetimeTuple(DateTuple('1970', '01', '01',
                                                         None, None, None),
                                               TimeTuple('00', '00',
                                                         '00.0000000000000000001',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1970', '01', '01',
                                                       None, None, None),
                                             TimeTuple('00', '00',
                                                       '09.0000000000000000009',
                                                       None))},
                       attotime.attodatetime(1970, 1, 1,
                                             nanosecond=
                                             Decimal('0.0000000001')),
                       attotime.attodatetime(1970, 1, 1,
                                             second=9,
                                             nanosecond=
                                             Decimal('0.0000000009'))))

        with localcontext() as context:
            context.prec = 30

            for testtuple in testtuples:
                result = AttoTimeBuilder.build_interval(**testtuple[0])
                self.assertEqual(result[0], testtuple[1])
                self.assertEqual(result[1], testtuple[2])

    def test_build_repeating_interval(self):
        args = {'Rnn': '3', 'interval': IntervalTuple(DateTuple('1981', '04', '05',
                                                                None, None, None),
                                                      None,
                                                     DurationTuple(None, None, None,
                                                                   '1', None, None,
                                                                   None))}
        results = list(AttoTimeBuilder.build_repeating_interval(**args))

        self.assertEqual(results[0], datetime.date(1981, 4, 5))
        self.assertEqual(results[1], datetime.date(1981, 4, 6))
        self.assertEqual(results[2], datetime.date(1981, 4, 7))

        args = {'Rnn': '11', 'interval': IntervalTuple(None,
                                                       DatetimeTuple(DateTuple('1980', '03', '05',
                                                                               None, None, None),
                                                                     TimeTuple('01', '01', '00',
                                                                               None)),
                                                       DurationTuple(None, None, None,
                                                                     None, '1', '2',
                                                                     None))}
        results = list(AttoTimeBuilder.build_repeating_interval(**args))

        for dateindex in compat.range(0, 11):
            self.assertEqual(results[dateindex],
                             attotime.attodatetime(1980, 3, 5, hour=1, minute=1)
                             - dateindex * attotime.attotimedelta(hours=1, minutes=2))

        args = {'Rnn': '2', 'interval': IntervalTuple(DatetimeTuple(DateTuple('1980', '03', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      DatetimeTuple(DateTuple('1981', '04', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      None)}
        results = list(AttoTimeBuilder.build_repeating_interval(**args))

        self.assertEqual(results[0],
                         attotime.attodatetime(1980, 3, 5, hour=1, minute=1))
        self.assertEqual(results[1],
                         attotime.attodatetime(1981, 4, 5, hour=1, minute=1))

        args = {'Rnn': '2', 'interval': IntervalTuple(DatetimeTuple(DateTuple('1980', '03', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      DatetimeTuple(DateTuple('1981', '04', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      None)}
        results = list(AttoTimeBuilder.build_repeating_interval(**args))

        self.assertEqual(results[0],
                         attotime.attodatetime(1980, 3, 5, hour=1, minute=1))
        self.assertEqual(results[1],
                         attotime.attodatetime(1981, 4, 5, hour=1, minute=1))

        args = {'R': True, 'interval': IntervalTuple(None,
                                                     DatetimeTuple(DateTuple('1980', '03', '05',
                                                                             None, None, None),
                                                                   TimeTuple('01', '01', '00',
                                                                             None)),
                                                     DurationTuple(None, None, None,
                                                                   None, '1', '2', None))}
        resultgenerator = AttoTimeBuilder.build_repeating_interval(**args)

        #Test the first 11 generated
        for dateindex in compat.range(0, 11):
            self.assertEqual(next(resultgenerator),
                             attotime.attodatetime(1980, 3, 5, hour=1, minute=1)
                             - dateindex * attotime.attotimedelta(hours=1, minutes=2))

    def test_date_generator(self):
        startdate = attotime.attodatetime(2018, 8, 29)
        duration = attotime.attotimedelta(nanoseconds=Decimal('0.1'))
        iterations = 10

        generator = AttoTimeBuilder._date_generator(startdate,
                                                    duration,
                                                    iterations)

        results = list(generator)

        for dateindex in compat.range(0, 10):
            self.assertEqual(results[dateindex],
                             startdate
                             + dateindex * duration)

        #Test date casting
        startdate = datetime.date(2018, 8, 29)
        duration = attotime.attotimedelta(days=1)
        iterations = 10

        generator = AttoTimeBuilder._date_generator(startdate,
                                                    duration,
                                                    iterations)

        results = list(generator)

        for dateindex in compat.range(0, 10):
            self.assertEqual(results[dateindex],
                             (attotime.attodatetime(2018, 8, 29)
                              + dateindex * duration).date())

    def test_date_generator_unbounded(self):
        startdate = attotime.attodatetime(2018, 8, 29)
        duration = -attotime.attotimedelta(nanoseconds=Decimal('0.5'))

        generator = AttoTimeBuilder._date_generator_unbounded(startdate,
                                                              duration)

        #Check the first 10 results
        for dateindex in compat.range(0, 10):
            self.assertEqual(next(generator),
                             startdate
                             + dateindex * duration)

        #Test date casting
        startdate = datetime.date(2018, 8, 29)
        duration = -attotime.attotimedelta(days=5)

        generator = AttoTimeBuilder._date_generator_unbounded(startdate,
                                                              duration)

        #Check the first 10 results
        for dateindex in compat.range(0, 10):
            self.assertEqual(next(generator),
                             (attotime.attodatetime(2018, 8, 29)
                             + dateindex * duration).date())
