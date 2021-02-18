# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import operator

import numpy as np

from decimal import Decimal
from aniso8601.builders import (BaseTimeBuilder, DateTuple, Limit,
                                TupleBuilder, cast)
from aniso8601.builders.python import PythonTimeBuilder
from aniso8601.exceptions import (DayOutOfBoundsError, HoursOutOfBoundsError,
                                  LeapSecondError, MidnightBoundsError,
                                  MinutesOutOfBoundsError, MonthOutOfBoundsError,
                                  SecondsOutOfBoundsError, WeekOutOfBoundsError,
                                  YearOutOfBoundsError)
from numpytimebuilder.constants import (DAYS_PER_MONTH, DAYS_PER_WEEK,
                                        DAYS_PER_YEAR)
from numpytimebuilder.util import apply_duration, decompose
from numpytimebuilder.version import __version__

def decimal_range_check(valuestr, limit):
    if valuestr is None:
        return None

    if '.' in valuestr:
        castfunc = Decimal
    else:
        castfunc = int

    value = cast(valuestr, castfunc, thrownmessage=limit.casterrorstring)

    if limit.min is not None and value < limit.min:
        raise limit.rangeexception(limit.rangeerrorstring)

    if limit.max is not None and value > limit.max:
        raise limit.rangeexception(limit.rangeerrorstring)

    return value

class NumPyTimeBuilder(BaseTimeBuilder):
    DURATION_PNY_LIMIT = Limit('Invalid year duration string.',
                               None, None, YearOutOfBoundsError,
                               None,
                               decimal_range_check)
    DURATION_PNM_LIMIT = Limit('Invalid month duration string.',
                               None, None, MonthOutOfBoundsError,
                               None,
                               decimal_range_check)
    DURATION_PNW_LIMIT = Limit('Invalid week duration string.',
                               None, None, WeekOutOfBoundsError,
                               None,
                               decimal_range_check)
    DURATION_PND_LIMIT = Limit('Invalid day duration string.',
                               None, None, DayOutOfBoundsError,
                               None,
                               decimal_range_check)
    DURATION_TNH_LIMIT = Limit('Invalid hour duration string.',
                               None, None, HoursOutOfBoundsError,
                               None,
                               decimal_range_check)
    DURATION_TNM_LIMIT = Limit('Invalid minute duration string.',
                               None, None, MinutesOutOfBoundsError,
                               None,
                               decimal_range_check)
    DURATION_TNS_LIMIT = Limit('Invalid second duration string.',
                               None, None, SecondsOutOfBoundsError,
                               None,
                               decimal_range_check)

    DURATION_RANGE_DICT = {'PnY': DURATION_PNY_LIMIT,
                           'PnM': DURATION_PNM_LIMIT,
                           'PnW': DURATION_PNW_LIMIT,
                           'PnD': DURATION_PND_LIMIT,
                           'TnH': DURATION_TNH_LIMIT,
                           'TnM': DURATION_TNM_LIMIT,
                           'TnS': DURATION_TNS_LIMIT}

    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None,
                   DDD=None):
        return np.datetime64(PythonTimeBuilder.build_date(YYYY=YYYY, MM=MM,
                                                          DD=DD, Www=Www,
                                                          D=D, DDD=DDD))

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        raise NotImplementedError('No compatible numpy time64 type.')

    @classmethod
    def build_datetime(cls, date, time):
        if time.tz is not None:
            raise NotImplementedError('Timezones are not supported by numpy '
                                      'datetime64 type.')

        cls.range_check_time(time.hh, time.mm, time.ss, time.tz, rangedict=cls.TIME_RANGE_DICT)

        hourstr = '00'
        minutestr = '00'
        secondstr = '00'

        fractionaldelta = None

        if time.hh is not None:
            if '.' in time.hh:
                hourstr = time.hh.split('.')[0].rjust(2, '0')

                fractionaldelta = cls.build_duration(TnH='.' + time.hh.split('.')[1])
            else:
                hourstr = time.hh.rjust(2, '0')

        if time.mm is not None:
            if '.' in time.mm:
                minutestr = time.mm.split('.')[0].rjust(2, '0')

                fractionaldelta = cls.build_duration(TnM='.' + time.mm.split('.')[1])
            else:
                minutestr = time.mm.rjust(2, '0')

        if time.ss is not None:
            if '.' in time.ss:
                secondstr = time.ss.split('.')[0].rjust(2, '0')

                fractionaldelta = cls.build_duration(TnS='.' + time.ss.split('.')[1])
            else:
                secondstr = time.ss.rjust(2, '0')

        date = cls.build_date(YYYY=date.YYYY, MM=date.MM, DD=date.DD,
                              Www=date.Www, D=date.D, DDD=date.DDD)

        #TODO: Add range checks for supported numpy spans
        #https://docs.scipy.org/doc/numpy/reference/arrays.datetime.html#datetime-units
        #https://github.com/numpy/numpy/pull/11873
        #https://github.com/numpy/numpy/issues/8161
        #https://github.com/numpy/numpy/issues/5452
        basedatetime = np.datetime64(str(date) + 'T' + hourstr + ':' + minutestr + ':' + secondstr)

        if fractionaldelta is not None:
            return apply_duration(basedatetime, fractionaldelta, operator.add)

        return basedatetime

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):
        #Build a delta for every numpy timedelta64 type
        years = Decimal(0)
        months = Decimal(0)
        days = Decimal(0)
        weeks = Decimal(0)
        hours = Decimal(0)
        minutes = Decimal(0)
        seconds = Decimal(0)

        PnY, PnM, PnW, PnD, TnH, TnM, TnS = cls.range_check_duration(PnY, PnM, PnW, PnD, TnH, TnM, TnS, rangedict=cls.DURATION_RANGE_DICT)

        if PnY is not None:
            years = PnY

        if PnM is not None:
            months = PnM

        if PnD is not None:
            days = PnD

        if PnW is not None:
            weeks = PnW

        if TnH is not None:
            hours = TnH

        if TnM is not None:
            minutes = TnM

        if TnS is not None:
            seconds = TnS

        #Convert years and months to days since numpy won't apply
        #year or month deltas to datetimes with day resolution
        days += years * DAYS_PER_YEAR
        days += months * DAYS_PER_MONTH

        #Convert weeks to days to save an argument
        days += weeks * DAYS_PER_WEEK

        return decompose(days, hours, minutes, seconds)

    @classmethod
    def build_interval(cls, start=None, end=None, duration=None):
        if start is not None and end is not None:
            #<start>/<end>
            #Handle concise format
            if cls._is_interval_end_concise(end) is True:
                end = cls._combine_concise_interval_tuples(start, end)

            startobject = cls._build_object(start)
            endobject = cls._build_object(end)

            return (startobject, endobject)

        durationobject = cls._build_object(duration)

        #Determine if datetime promotion is required, forced to boolean
        #because numpy comparisons result in 1d arrays
        datetimerequired = bool(duration[4] is not None
                                or duration[5] is not None
                                or duration[6] is not None
                                or durationobject[1] != np.timedelta64(0)
                                or durationobject[2] != np.timedelta64(0)
                                or durationobject[3] != np.timedelta64(0)
                                or durationobject[4] != np.timedelta64(0)
                                or durationobject[5] != np.timedelta64(0)
                                or durationobject[6] != np.timedelta64(0)
                                or durationobject[7] != np.timedelta64(0)
                                or durationobject[8] != np.timedelta64(0)
                                or durationobject[9] != np.timedelta64(0))

        if end is not None:
            #<duration>/<end>
            endobject = cls._build_object(end)

            if type(end) is DateTuple and datetimerequired is True:
                #<end> is a date, and <duration> requires datetime resolution
                nulltime = TupleBuilder.build_time() #Time for elapsed datetime

                return (endobject,
                        apply_duration(cls.build_datetime(end, nulltime),
                                       durationobject, operator.sub))

            return (endobject,
                    apply_duration(endobject,
                                   durationobject, operator.sub))

        #<start>/<duration>
        startobject = cls._build_object(start)

        if type(start) is DateTuple and datetimerequired is True:
            #<start> is a date, and <duration> requires datetime resolution
            nulltime = TupleBuilder.build_time() #Time for elapsed datetime

            return (startobject,
                    apply_duration(cls.build_datetime(start, nulltime),
                                   durationobject, operator.add))

        return (startobject,
                apply_duration(startobject,
                               durationobject, operator.add))

    @classmethod
    def build_repeating_interval(cls, R=None, Rnn=None, interval=None):
        startobject = None
        endobject = None

        R, Rnn, interval = cls.range_check_repeating_interval(R, Rnn, interval, rangedict=cls.REPEATING_INTERVAL_RANGE_DICT)

        if interval.start is not None:
            startobject = cls._build_object(interval.start)

        if interval.end is not None:
            endobject = cls._build_object(interval.end)

        if interval.duration is not None:
            durationobject = cls._build_object(interval.duration)
        else:
            #Generator builders use apply_duration internally, which requires
            #a tuple of timedelta64 objects
            durationobject = ((endobject - startobject),)

        if R is True:
            if startobject is not None:
                return cls._date_generator_unbounded(startobject,
                                                     durationobject,
                                                     operator.add)

            return cls._date_generator_unbounded(endobject,
                                                 durationobject,
                                                 operator.sub)

        if startobject is not None:
            return cls._date_generator(startobject, durationobject,
                                       Rnn, operator.add)

        return cls._date_generator(endobject, durationobject,
                                   Rnn, operator.sub)

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        raise NotImplementedError('Timezones are not supported by '
                                  'numpy datetime64 type.')

    @staticmethod
    def _date_generator(startdate, duration, iterations, op):
        currentdate = startdate
        currentiteration = 0

        while currentiteration < iterations:
            yield currentdate

            #Update the values
            currentdate = apply_duration(currentdate, duration, op)
            currentiteration += 1

    @staticmethod
    def _date_generator_unbounded(startdate, duration, op):
        currentdate = startdate

        while True:
            yield currentdate

            #Update the value
            currentdate = apply_duration(currentdate, duration, op)
