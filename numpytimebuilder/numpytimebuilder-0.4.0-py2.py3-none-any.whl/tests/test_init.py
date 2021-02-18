# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import operator
import unittest

import numpy as np

from aniso8601 import compat
from aniso8601.builders import (DateTuple, DatetimeTuple,
                                DurationTuple, IntervalTuple,
                                TimeTuple, TimezoneTuple)
from aniso8601.exceptions import (DayOutOfBoundsError, LeapSecondError,
                                  MinutesOutOfBoundsError,
                                  SecondsOutOfBoundsError,
                                  WeekOutOfBoundsError, YearOutOfBoundsError)
from numpytimebuilder import NumPyTimeBuilder

class TestNumPyTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        testtuples = (({'YYYY': '2013', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       np.datetime64(datetime.date(2013, 1, 1))),
                      ({'YYYY': '0001', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       np.datetime64(datetime.date(1, 1, 1))),
                      ({'YYYY': '1900', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       np.datetime64(datetime.date(1900, 1, 1))),
                      ({'YYYY': '1981', 'MM': '04', 'DD': '05', 'Www': None,
                        'D': None, 'DDD': None},
                       np.datetime64(datetime.date(1981, 4, 5))),
                      ({'YYYY': '1981', 'MM': '04', 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       np.datetime64(datetime.date(1981, 4, 1))),
                      ({'YYYY': '1981', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': '095'},
                       np.datetime64(datetime.date(1981, 4, 5))),
                      ({'YYYY': '1981', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': '365'},
                       np.datetime64(datetime.date(1981, 12, 31))),
                      ({'YYYY': '1980', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': '366'},
                       np.datetime64(datetime.date(1980, 12, 31))),
                      #Make sure we shift in zeros
                      ({'YYYY': '1', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       np.datetime64(datetime.date(1000, 1, 1))),
                      ({'YYYY': '12', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       np.datetime64(datetime.date(1200, 1, 1))),
                      ({'YYYY': '123', 'MM': None, 'DD': None, 'Www': None,
                        'D': None, 'DDD': None},
                       np.datetime64(datetime.date(1230, 1, 1))))

        for testtuple in testtuples:
            result = NumPyTimeBuilder.build_date(**testtuple[0])
            self.assertEqual(result, testtuple[1])

        #Test weekday
        testtuples = (({'YYYY': '2004', 'MM': None, 'DD': None, 'Www': '53',
                        'D': None, 'DDD': None},
                       np.datetime64('2004-12-27')),
                      ({'YYYY': '2009', 'MM': None, 'DD': None, 'Www': '01',
                        'D': None, 'DDD': None},
                       np.datetime64('2008-12-29')),
                      ({'YYYY': '2010', 'MM': None, 'DD': None, 'Www': '01',
                        'D': None, 'DDD': None},
                       np.datetime64('2010-01-04')),
                      ({'YYYY': '2009', 'MM': None, 'DD': None, 'Www': '53',
                        'D': None, 'DDD': None},
                       np.datetime64('2009-12-28')),
                      ({'YYYY': '2009', 'MM': None, 'DD': None, 'Www': '01',
                        'D': '1', 'DDD': None},
                       np.datetime64('2008-12-29')),
                      ({'YYYY': '2009', 'MM': None, 'DD': None, 'Www': '53',
                        'D': '7', 'DDD': None},
                       np.datetime64('2010-01-03')),
                      ({'YYYY': '2010', 'MM': None, 'DD': None, 'Www': '01',
                        'D': '1', 'DDD': None},
                       np.datetime64('2010-01-04')),
                      ({'YYYY': '2004', 'MM': None, 'DD': None, 'Www': '53',
                        'D': '6', 'DDD': None},
                       np.datetime64('2005-01-01')))

        for testtuple in testtuples:
            result = NumPyTimeBuilder.build_date(**testtuple[0])
            self.assertEqual(result, testtuple[1])

    def test_build_date_bounds_checking(self):
        #0 isn't a valid week number
        with self.assertRaises(WeekOutOfBoundsError):
            NumPyTimeBuilder.build_date(YYYY='2003', Www='00')

        #Week must not be larger than 53
        with self.assertRaises(WeekOutOfBoundsError):
            NumPyTimeBuilder.build_date(YYYY='2004', Www='54')

        #0 isn't a valid day number
        with self.assertRaises(DayOutOfBoundsError):
            NumPyTimeBuilder.build_date(YYYY='2001', Www='02', D='0')

        #Day must not be larger than 7
        with self.assertRaises(DayOutOfBoundsError):
            NumPyTimeBuilder.build_date(YYYY='2001', Www='02', D='8')

        #0 isn't a valid year for a Python builder
        with self.assertRaises(YearOutOfBoundsError):
            NumPyTimeBuilder.build_date(YYYY='0000')

        with self.assertRaises(DayOutOfBoundsError):
            NumPyTimeBuilder.build_date(YYYY='1981', DDD='000')

        #Day 366 is only valid on a leap year
        with self.assertRaises(DayOutOfBoundsError):
            NumPyTimeBuilder.build_date(YYYY='1981', DDD='366')

        #Day must me 365, or 366, not larger
        with self.assertRaises(DayOutOfBoundsError):
            NumPyTimeBuilder.build_date(YYYY='1981', DDD='367')

    def test_build_time(self):
        with self.assertRaises(NotImplementedError):
            NumPyTimeBuilder.build_time()

    def test_build_datetime(self):
        testtuples = (((DateTuple('1234', '2', '3', None, None, None),
                        TimeTuple('23', '21', '28.512400', None)),
                       np.datetime64('1234-02-03T23:21:28.512400')),
                      ((DateTuple('1234', '2', '3', None, None, None),
                        TimeTuple('23', '21', '59.9999997', None)),
                       np.datetime64('1234-02-03T23:21:59.9999997')),
                      ((DateTuple('1234', '2', '3', None, None, None),
                        TimeTuple('23.9999997', None, None, None)),
                       np.datetime64('1234-02-03T23:59:59.998920')),
                      ((DateTuple('1981', '4', '5', None, None, None),
                        TimeTuple('23', '21', '59.000000001', None)),
                       np.datetime64('1981-04-05'
                                     'T23:21:59.000000001')),
                      ((DateTuple('2006', '11', '23', None, None, None),
                        TimeTuple('01', '02', '03.999999999', None)),
                       np.datetime64('2006-11-23'
                                     'T01:02:03.999999999')),
                      ((DateTuple('1970', '01', '01', None, None, None),
                        TimeTuple('00', '00', '00.000000000000001', None)),
                       np.datetime64('1970-01-01'
                                     'T00:00:00.000000000000001')),
                      ((DateTuple('1970', '01', '01', None, None, None),
                        TimeTuple('00', '00', '09.000000000000009', None)),
                       np.datetime64('1970-01-01'
                                     'T00:00:09.000000000000009')))

        for testtuple in testtuples:
            result = NumPyTimeBuilder.build_datetime(*testtuple[0])
            self.assertEqual(result, testtuple[1])

    def test_build_datetime_timezone(self):
        with self.assertRaises(NotImplementedError):
            NumPyTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                             None, None, None),
                                            TimeTuple('23', '21', '28.512400',
                                                      TimezoneTuple(False,
                                                                    None,
                                                                    '11',
                                                                    '15',
                                                                    '+11:15')))

    def test_build_datetime_bounds_checking(self):
        #Leap seconds not supported
        with self.assertRaises(LeapSecondError):
            NumPyTimeBuilder.build_datetime(DateTuple('2016', '12', '31',
                                                      None, None, None),
                                            TimeTuple('23', '59', '60', None))

        with self.assertRaises(SecondsOutOfBoundsError):
            NumPyTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                      None, None, None),
                                            TimeTuple('00', '00', '60', None))

        with self.assertRaises(SecondsOutOfBoundsError):
            NumPyTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                      None, None, None),
                                            TimeTuple('00', '00', '61', None))

        with self.assertRaises(SecondsOutOfBoundsError):
            NumPyTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                      None, None, None),
                                            TimeTuple('00', '59', '61', None))

        with self.assertRaises(MinutesOutOfBoundsError):
            NumPyTimeBuilder.build_datetime(DateTuple('1981', '04', '05',
                                                      None, None, None),
                                            TimeTuple('00', '61', None, None))

    def test_build_duration(self):
        testtuples = (({'PnY': '1', 'PnM': '2', 'PnD': '3',
                        'TnH': '4', 'TnM': '54', 'TnS': '6'},
                       (np.timedelta64(428, 'D'),
                        np.timedelta64(4, 'h'),
                        np.timedelta64(54, 'm'),
                        np.timedelta64(6, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3',
                        'TnH': '4', 'TnM': '54', 'TnS': '6.5'},
                       (np.timedelta64(428, 'D'),
                        np.timedelta64(4, 'h'),
                        np.timedelta64(54, 'm'),
                        np.timedelta64(6, 's'),
                        np.timedelta64(500, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3'},
                       (np.timedelta64(428, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3.5'},
                       (np.timedelta64(428, 'D'),
                        np.timedelta64(12, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'TnH': '4', 'TnM': '54', 'TnS': '6.5'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(4, 'h'),
                        np.timedelta64(54, 'm'),
                        np.timedelta64(6, 's'),
                        np.timedelta64(500, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'TnS': '0.0000001'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(100, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'TnS': '2.0000048'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(2, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(4, 'us'),
                        np.timedelta64(800, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'TnS': '0.000000000000000001'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(1, 'as'))),
                      ({'PnY': '1'},
                       (np.timedelta64(365, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnY': '1.5'},
                       (np.timedelta64(547, 'D'),
                        np.timedelta64(12, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnM': '1'},
                       (np.timedelta64(30, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnM': '1.5'},
                       (np.timedelta64(45, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnW': '1'},
                       (np.timedelta64(7, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnW': '1.5'},
                       (np.timedelta64(10, 'D'),
                        np.timedelta64(12, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnD': '1'},
                       (np.timedelta64(1, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnD': '1.5'},
                       (np.timedelta64(1, 'D'),
                        np.timedelta64(12, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnY': '0003', 'PnM': '06', 'PnD': '04',
                        'TnH': '12', 'TnM': '30', 'TnS': '05'},
                       (np.timedelta64(1279, 'D'),
                        np.timedelta64(12, 'h'),
                        np.timedelta64(30, 'm'),
                        np.timedelta64(5, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'PnY': '0003', 'PnM': '06', 'PnD': '04',
                        'TnH': '12', 'TnM': '30', 'TnS': '05.5'},
                       (np.timedelta64(1279, 'D'),
                        np.timedelta64(12, 'h'),
                        np.timedelta64(30, 'm'),
                        np.timedelta64(5, 's'),
                        np.timedelta64(500, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      ({'TnH': '4', 'TnM': '54', 'TnS': '28.512400'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(4, 'h'),
                        np.timedelta64(54, 'm'),
                        np.timedelta64(28, 's'),
                        np.timedelta64(512, 'ms'),
                        np.timedelta64(400, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(0, 'as'))),
                      #Make sure we truncate, not round
                      ({'PnY': '1999.999999999999999999999999'},
                       (np.timedelta64(729999, 'D'),
                        np.timedelta64(23, 'h'),
                        np.timedelta64(59, 'm'),
                        np.timedelta64(59, 's'),
                        np.timedelta64(999, 'ms'),
                        np.timedelta64(999, 'us'),
                        np.timedelta64(999, 'ns'),
                        np.timedelta64(999, 'ps'),
                        np.timedelta64(999, 'fs'),
                        np.timedelta64(965, 'as'))),
                      ({'PnM': '1.9999999999999999999999999'},
                       (np.timedelta64(59, 'D'),
                        np.timedelta64(23, 'h'),
                        np.timedelta64(59, 'm'),
                        np.timedelta64(59, 's'),
                        np.timedelta64(999, 'ms'),
                        np.timedelta64(999, 'us'),
                        np.timedelta64(999, 'ns'),
                        np.timedelta64(999, 'ps'),
                        np.timedelta64(999, 'fs'),
                        np.timedelta64(999, 'as'))),
                      ({'PnW': '1.999999999999999999999999'},
                       (np.timedelta64(13, 'D'),
                        np.timedelta64(23, 'h'),
                        np.timedelta64(59, 'm'),
                        np.timedelta64(59, 's'),
                        np.timedelta64(999, 'ms'),
                        np.timedelta64(999, 'us'),
                        np.timedelta64(999, 'ns'),
                        np.timedelta64(999, 'ps'),
                        np.timedelta64(999, 'fs'),
                        np.timedelta64(999, 'as'))),
                      ({'PnD': '1.99999999999999999999999'},
                       (np.timedelta64(1, 'D'),
                        np.timedelta64(23, 'h'),
                        np.timedelta64(59, 'm'),
                        np.timedelta64(59, 's'),
                        np.timedelta64(999, 'ms'),
                        np.timedelta64(999, 'us'),
                        np.timedelta64(999, 'ns'),
                        np.timedelta64(999, 'ps'),
                        np.timedelta64(999, 'fs'),
                        np.timedelta64(999, 'as'))),
                      ({'TnH': '0.0000000000000000099999'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(35, 'fs'),
                        np.timedelta64(999, 'as'))),
                      ({'TnM': '0.00000000000000000999'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(599, 'as'))),
                      ({'TnS': '0.0000000000000000011'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(1, 'as'))),
                      ({'TnS': '0.0000000000000000099'},
                       (np.timedelta64(0, 'D'),
                        np.timedelta64(0, 'h'),
                        np.timedelta64(0, 'm'),
                        np.timedelta64(0, 's'),
                        np.timedelta64(0, 'ms'),
                        np.timedelta64(0, 'us'),
                        np.timedelta64(0, 'ns'),
                        np.timedelta64(0, 'ps'),
                        np.timedelta64(0, 'fs'),
                        np.timedelta64(9, 'as'))))

        for testtuple in testtuples:
            result = NumPyTimeBuilder.build_duration(**testtuple[0])
            self.assertEqual(result, testtuple[1])

    def test_build_interval(self):
        testtuples = (({'end': DatetimeTuple(DateTuple('1981', '04', '05', None, None, None),
                                             TimeTuple('01', '01', '00', None)),
                        'duration': DurationTuple(None, '1', None, None, None, None, None)},
                       np.datetime64('1981-04-05T01:01:00'),
                       np.datetime64('1981-03-06T01:01:00')),
                      ({'end': DateTuple('1981', '04', '05', None, None, None),
                        'duration': DurationTuple(None, '1', None, None, None, None, None)},
                       np.datetime64('1981-04-05'),
                       np.datetime64('1981-03-06')),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple('1.5', None, None, None, None, None, None)},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2016-09-04T12:00:00')),
                      ({'end': DateTuple('2014', '11', '12', None, None, None),
                        'duration': DurationTuple(None, None, None, None, '1', None, None)},
                       np.datetime64('2014-11-12'),
                       np.datetime64('2014-11-11T23:00:00')),
                      ({'end': DateTuple('2014', '11', '12', None, None, None),
                        'duration': DurationTuple(None, None, None, None, '4', '54', '6.5')},
                       np.datetime64('2014-11-12'),
                       np.datetime64('2014-11-11T19:05:53.5')),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000001')},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-03-05T23:59:59.9999999')),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000048')},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-03-05T23:59:57.9999952')),
                      #Make sure we truncate, not round
                      ({'end': DateTuple('2000', '01', '01',
                                         None, None, None),
                        'duration': DurationTuple('1999.999999999', None, None,
                                                  None, None, None,
                                                  None)},
                       np.datetime64('2000-01-01'),
                       np.datetime64('0001-04-30T00:00:00.031536')),
                      ({'end': DateTuple('1989', '03', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, '1.999999999999', None,
                                                  None, None, None,
                                                  None)},
                       np.datetime64('1989-03-01'),
                       np.datetime64('1988-12-31T00:00:00.000002592')),
                      ({'end': DateTuple('1989', '03', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, '1.99999999999',
                                                  None, None, None,
                                                  None)},
                       np.datetime64('1989-03-01'),
                       np.datetime64('1989-02-15T00:00:00.000006048')),
                      ({'end': DateTuple('1989', '03', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  '1.99999999999', None, None,
                                                  None)},
                       np.datetime64('1989-03-01'),
                       np.datetime64('1989-02-27T00:00:00.000000864')),
                      ({'end': DateTuple('2001', '01', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '14.99999999999', None,
                                                  None)},
                       np.datetime64('2001-01-01'),
                       np.datetime64('2000-12-31T09:00:00.000000036')),
                      ({'end': DateTuple('2001', '01', '01',
                                         None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, '0.0000000999',
                                                  None)},
                       np.datetime64('2001-01-01'),
                       np.datetime64('2000-12-31T23:59:59.999994006')),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000000000000000001')},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-03-06')),
                      ({'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000000000000000009')},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-03-05T23:59:58')),
                      ({'start': DatetimeTuple(DateTuple('1981', '04', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00', None)),
                        'duration': DurationTuple(None, '1', None,
                                                  '1', None, '1', None)},
                       np.datetime64('1981-04-05T01:01:00'),
                       np.datetime64('1981-05-06T01:02:00')),
                      ({'start': DateTuple('1981', '04', '05',
                                           None, None, None),
                        'duration': DurationTuple(None, '1', None,
                                                  '1', None, None, None)},
                       np.datetime64('1981-04-05'),
                       np.datetime64('1981-05-06')),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, '2.5', None,
                                                  None, None, None, None)},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-05-20')),
                      ({'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '1', None, None)},
                       np.datetime64('2014-11-12'),
                       np.datetime64('2014-11-12T01:00:00')),
                      ({'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '4', '54', '6.5')},
                       np.datetime64('2014-11-12'),
                       np.datetime64('2014-11-12T04:54:06.5')),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000001')},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-03-06T00:00:00.0000001')),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000048')},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-03-06T00:00:02.0000048')),
                      #Make sure we truncate, not round
                      ({'start': DateTuple('2000', '01', '01',
                                           None, None, None),
                        'duration': DurationTuple('1999.999999999', None, None,
                                                  None, None, None,
                                                  None)},
                       np.datetime64('2000-01-01'),
                       np.datetime64('3998-09-02T23:59:59.968464')),
                      ({'start': DateTuple('1989', '03', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, '1.999999999999', None,
                                                  None, None, None,
                                                  None)},
                       np.datetime64('1989-03-01'),
                       np.datetime64('1989-04-29T23:59:59.999997408')),
                      ({'start': DateTuple('1989', '03', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, '1.99999999999',
                                                  None, None, None,
                                                  None)},
                       np.datetime64('1989-03-01'),
                       np.datetime64('1989-03-14T23:59:59.999993952')),
                      ({'start': DateTuple('1989', '03', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  '1.99999999999', None, None,
                                                  None)},
                       np.datetime64('1989-03-01'),
                       np.datetime64('1989-03-02T23:59:59.999999136')),
                      ({'start': DateTuple('2001', '01', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '14.99999999999', None,
                                                  None)},
                       np.datetime64('2001-01-01'),
                       np.datetime64('2001-01-01T14:59:59.999999964')),
                      ({'start': DateTuple('2001', '01', '01',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, '0.0000000999',
                                                  None)},
                       np.datetime64('2001-01-01'),
                       np.datetime64('2001-01-01T00:00:00.000005994')),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000000000000000001')},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-03-06')),
                      ({'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000000000000000009')},
                       np.datetime64('2018-03-06'),
                       np.datetime64('2018-03-06T00:00:02')),
                      ({'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))},
                       np.datetime64('1980-03-05T01:01:00'),
                       np.datetime64('1981-04-05T01:01:00')),
                      ({'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DateTuple('1981', '04', '05',
                                         None, None, None)},
                       np.datetime64('1980-03-05T01:01:00'),
                       np.datetime64('1981-04-05')),
                      ({'start': DateTuple('1980', '03', '05',
                                           None, None, None),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))},
                       np.datetime64('1980-03-05'),
                       np.datetime64('1981-04-05T01:01:00')),
                      ({'start': DateTuple('1980', '03', '05',
                                           None, None, None),
                        'end': DateTuple('1981', '04', '05',
                                         None, None, None)},
                       np.datetime64('1980-03-05'),
                       np.datetime64('1981-04-05')),
                      ({'start': DateTuple('1981', '04', '05',
                                           None, None, None),
                        'end': DateTuple('1980', '03', '05',
                                         None, None, None)},
                       np.datetime64('1981-04-05'),
                       np.datetime64('1980-03-05')),
                      ({'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00.0000001',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('14', '43', '59.9999997', None))},
                       np.datetime64('1980-03-05T01:01:00.0000001'),
                       np.datetime64('1981-04-05T14:43:59.9999997')),
                      #Test concise representation
                      ({'start': DateTuple('2020', '01', '01',
                                           None, None, None),
                        'end': DateTuple(None, None, '02',
                                         None, None, None)},
                        np.datetime64('2020-01-01'),
                        np.datetime64('2020-01-02')),
                      ({'start': DateTuple('2008', '02', '15',
                                           None, None, None),
                        'end': DateTuple(None, '03', '14',
                                         None, None, None)},
                        np.datetime64('2008-02-15'),
                        np.datetime64('2008-03-14')),
                      ({'start': DatetimeTuple(DateTuple('2007', '12', '14',
                                                         None, None, None),
                                               TimeTuple('13', '30', None,
                                                         None)),
                        'end': TimeTuple('15', '30', None,
                                         None)},
                        np.datetime64('2007-12-14T13:30'),
                        np.datetime64('2007-12-14T15:30')),
                      ({'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         None)),
                        'end': DatetimeTuple(DateTuple(None, None, '15',
                                                       None, None, None),
                                             TimeTuple('17', '00', None,
                                                       None))},
                        np.datetime64('2007-11-13T09:00'),
                        np.datetime64('2007-11-15T17:00')),
                      ({'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('00', '00', None,
                                                         None)),
                        'end': DatetimeTuple(DateTuple(None, None, '16',
                                                       None, None, None),
                                             TimeTuple('00', '00', None,
                                                       None))},
                        np.datetime64('2007-11-13'),
                        np.datetime64('2007-11-16')),
                      ({'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         None)),
                        'end': TimeTuple('12', '34.567', None,
                                         None)},
                       np.datetime64('2007-11-13T09:00'),
                       np.datetime64('2007-11-13T12:34:34.020')),
                      ({'start': DateTuple('2007', '11', '13',
                                           None, None, None),
                        'end': TimeTuple('12', '34', None,
                                         None)},
                        np.datetime64('2007-11-13'),
                        np.datetime64('2007-11-13T12:34')),
                      #Make sure we truncate, not round
                      ({'start': DatetimeTuple(DateTuple('1970', '01', '01',
                                                         None, None, None),
                                               TimeTuple('00', '00', '00.0000000000000000001',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1970', '01', '01',
                                                       None, None, None),
                                             TimeTuple('00', '00', '09.0000000000000000009',
                                                       None))},
                       np.datetime64('1970-01-01'
                                     'T00:00:00.00'),
                       np.datetime64('1970-01-01'
                                     'T00:00:09.00')))

        for testtuple in testtuples:
            result = NumPyTimeBuilder.build_interval(**testtuple[0])
            self.assertEqual(result[0], testtuple[1])
            self.assertEqual(result[1], testtuple[2])

    def test_build_repeating_interval(self):
        args = {'Rnn': '3', 'interval': IntervalTuple(DateTuple('1981', '04', '05',
                                                                None, None, None),
                                                      None,
                                                     DurationTuple(None, None, None,
                                                                   '1', None, None,
                                                                   None))}
        results = list(NumPyTimeBuilder.build_repeating_interval(**args))

        self.assertEqual(results[0], np.datetime64('1981-04-05'))
        self.assertEqual(results[1], np.datetime64('1981-04-06'))
        self.assertEqual(results[2], np.datetime64('1981-04-07'))

        args = {'Rnn': '11', 'interval': IntervalTuple(None,
                                                       DatetimeTuple(DateTuple('1980', '03', '05',
                                                                               None, None, None),
                                                                     TimeTuple('01', '01', '00',
                                                                               None)),
                                                       DurationTuple(None, None, None,
                                                                     None, '1', '2',
                                                                     None))}
        results = list(NumPyTimeBuilder.build_repeating_interval(**args))

        for dateindex in compat.range(0, 11):
            self.assertEqual(results[dateindex],
                             np.datetime64('1980-03-05T01:01:00')
                             - dateindex * np.timedelta64(1, 'h')
                             - dateindex * np.timedelta64(2, 'm'))

        args = {'Rnn': '2', 'interval': IntervalTuple(DatetimeTuple(DateTuple('1980', '03', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      DatetimeTuple(DateTuple('1981', '04', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      None)}
        results = list(NumPyTimeBuilder.build_repeating_interval(**args))

        self.assertEqual(results[0],
                         np.datetime64('1980-03-05T01:01:00'))
        self.assertEqual(results[1],
                         np.datetime64('1981-04-05T01:01:00'))

        args = {'Rnn': '2', 'interval': IntervalTuple(DatetimeTuple(DateTuple('1980', '03', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      DatetimeTuple(DateTuple('1981', '04', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      None)}
        results = list(NumPyTimeBuilder.build_repeating_interval(**args))

        self.assertEqual(results[0],
                         np.datetime64('1980-03-05T01:01:00'))
        self.assertEqual(results[1],
                         np.datetime64('1981-04-05T01:01:00'))

        args = {'R': True, 'interval': IntervalTuple(None,
                                                     DatetimeTuple(DateTuple('1980', '03', '05',
                                                                             None, None, None),
                                                                   TimeTuple('01', '01', '00',
                                                                             None)),
                                                     DurationTuple(None, None, None,
                                                                   None, '1', '2', None))}
        resultgenerator = NumPyTimeBuilder.build_repeating_interval(**args)

        #Test the first 11 generated
        for dateindex in compat.range(0, 11):
            self.assertEqual(next(resultgenerator),
                             np.datetime64('1980-03-05T01:01:00')
                             - dateindex * np.timedelta64(1, 'h')
                             - dateindex * np.timedelta64(2, 'm'))

    def test_build_timezone(self):
        with self.assertRaises(NotImplementedError):
            NumPyTimeBuilder.build_timezone()

    def test_date_generator(self):
        startdate = np.datetime64('2018-08-29')
        duration = (np.timedelta64(1, 'D'),)
        iterations = 10

        generator = NumPyTimeBuilder._date_generator(startdate,
                                                     duration,
                                                     iterations,
                                                     operator.add)

        results = list(generator)

        for dateindex in compat.range(0, 10):
            self.assertEqual(results[dateindex],
                             startdate
                             + dateindex * duration[0])

    def test_date_generator_unbounded(self):
        startdate = np.datetime64('2018-08-29')
        duration = (np.timedelta64(5, 'D'),)

        generator = NumPyTimeBuilder._date_generator_unbounded(startdate,
                                                               duration,
                                                               operator.sub)

        #Check the first 10 results
        for dateindex in compat.range(0, 10):
            self.assertEqual(next(generator),
                             startdate
                             - dateindex * duration[0])
