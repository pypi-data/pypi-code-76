# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import attotime

from decimal import Decimal
from aniso8601.builders import (BaseTimeBuilder, DateTuple,
                                Limit, TupleBuilder,
                                cast)
from aniso8601.builders.python import PythonTimeBuilder
from aniso8601.exceptions import (DayOutOfBoundsError, HoursOutOfBoundsError,
                                  LeapSecondError, MidnightBoundsError,
                                  MinutesOutOfBoundsError, MonthOutOfBoundsError,
                                  SecondsOutOfBoundsError, WeekOutOfBoundsError,
                                  YearOutOfBoundsError)
from attotimebuilder.version import __version__

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

class AttoTimeBuilder(PythonTimeBuilder):
    TIME_HH_LIMIT = Limit('Invalid hour string.',
                          0, 24, HoursOutOfBoundsError,
                          'Hour must be between 0..24 with '
                          '24 representing midnight.',
                          decimal_range_check)
    TIME_MM_LIMIT = Limit('Invalid minute string.',
                          0, 59, MinutesOutOfBoundsError,
                          'Minute must be between 0..59.',
                          decimal_range_check)
    TIME_SS_LIMIT = Limit('Invalid second string.',
                          0, 60, SecondsOutOfBoundsError,
                          'Second must be between 0..60 with '
                          '60 representing a leap second.',
                          decimal_range_check)
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

    TIME_RANGE_DICT = {'hh': TIME_HH_LIMIT, 'mm': TIME_MM_LIMIT, 'ss': TIME_SS_LIMIT}

    DURATION_RANGE_DICT = {'PnY': DURATION_PNY_LIMIT,
                           'PnM': DURATION_PNM_LIMIT,
                           'PnW': DURATION_PNW_LIMIT,
                           'PnD': DURATION_PND_LIMIT,
                           'TnH': DURATION_TNH_LIMIT,
                           'TnM': DURATION_TNM_LIMIT,
                           'TnS': DURATION_TNS_LIMIT}

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        #Builds a time from the given parts, handling fractional arguments
        #where necessary
        hours = 0
        minutes = 0
        seconds = 0

        decimalhours = Decimal(0)
        decimalminutes = Decimal(0)
        decimalseconds = Decimal(0)

        hh, mm, ss, tz = cls.range_check_time(hh, mm, ss, tz)

        if hh is not None:
            if type(hh) is Decimal:
                decimalhours = hh
                hours = 0
            else:
                hours = hh

        if mm is not None:
            if type(mm) is Decimal:
                decimalminutes = mm
                minutes = 0
            else:
                minutes = mm

        if ss is not None:
            if type(ss) is Decimal:
                decimalseconds = ss
                seconds = 0
            else:
                seconds = ss

        #Fix ranges that have passed range checks
        if hours == 24:
            hours = 0
            minutes = 0
            seconds = 0

        #Datetimes don't handle fractional components, so we use a timedelta
        if tz is not None:
            return (attotime.attodatetime(1, 1, 1,
                                          hour=hours,
                                          minute=minutes,
                                          second=seconds,
                                          tzinfo=cls._build_object(tz))
                    + attotime.attotimedelta(hours=decimalhours,
                                             minutes=decimalminutes,
                                             seconds=decimalseconds)
                   ).timetz()

        return (attotime.attodatetime(1, 1, 1,
                                      hour=hours,
                                      minute=minutes,
                                      second=seconds)
                + attotime.attotimedelta(hours=decimalhours,
                                         minutes=decimalminutes,
                                         seconds=decimalseconds)
               ).time()

    @classmethod
    def build_datetime(cls, date, time):
        return attotime.attodatetime.combine(cls._build_object(date),
                                             cls._build_object(time))

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):
        years = 0
        months = 0
        weeks = 0
        days = 0
        hours = 0
        minutes = 0
        seconds = 0

        PnY, PnM, PnW, PnD, TnH, TnM, TnS = BaseTimeBuilder.range_check_duration(PnY, PnM, PnW, PnD, TnH, TnM, TnS, rangedict=cls.DURATION_RANGE_DICT)

        if PnY is not None:
            years = PnY

        if PnM is not None:
            months = PnM

        if PnW is not None:
            weeks = PnW

        if PnD is not None:
            days = PnD

        if TnH is not None:
            hours = TnH

        if TnM is not None:
            minutes = TnM

        if TnS is not None:
            seconds = TnS

        #Note that weeks can be handled without conversion to days
        totaldays = years * 365 + months * 30 + days

        return attotime.attotimedelta(days=totaldays,
                                      seconds=seconds,
                                      minutes=minutes,
                                      hours=hours,
                                      weeks=weeks)

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

        #Determine if datetime promotion is required
        datetimerequired = (duration[4] is not None
                            or duration[5] is not None
                            or duration[6] is not None
                            or durationobject.seconds != 0
                            or durationobject.microseconds != 0
                            or durationobject.nanoseconds != 0)

        if end is not None:
            #<duration>/<end>
            endobject = cls._build_object(end)
            if type(end) is DateTuple:
                enddatetime = cls.build_datetime(end, TupleBuilder.build_time())

                if datetimerequired is True:
                    #<end> is a date, and <duration> requires datetime resolution
                    return (endobject,
                            enddatetime - durationobject)

                #<end> is a date, but attotimedeltas can only be applied
                #to attodatetimes
                return (endobject,
                        (enddatetime - durationobject).date())

            return (endobject,
                    endobject
                    - durationobject)

        #<start>/<duration>
        startobject = cls._build_object(start)

        if type(start) is DateTuple:
            startdatetime = cls.build_datetime(start, TupleBuilder.build_time())

            if datetimerequired is True:
                #<start> is a date, and <duration> requires datetime resolution
                return (startobject,
                        startdatetime + durationobject)

            #<start> is a date, but attotimedeltas can only be applied
            #to attodatetimes
            return (startobject,
                    (startdatetime + durationobject).date())

        return (startobject,
                startobject
                + durationobject)

    @staticmethod
    def _date_generator(start, timedelta, iterations):
        if isinstance(start, datetime.date):
            #No attodate object compatible with attotimedelta, so convert
            #to attodatetime
            current = attotime.attodatetime(year=start.year,
                                            month=start.month,
                                            day=start.day)
            returnasdate = True
        else:
            current = start
            returnasdate = False

        currentiteration = 0

        while currentiteration < iterations:
            if returnasdate is True:
                yield current.date()
            else:
                yield current

            #Update the values
            current += timedelta
            currentiteration += 1

    @staticmethod
    def _date_generator_unbounded(start, timedelta):
        if isinstance(start, datetime.date):
            #No attodate object compatible with attotimedelta, so convert
            #to attodatetime
            current = attotime.attodatetime(year=start.year,
                                            month=start.month,
                                            day=start.day)
            returnasdate = True
        else:
            current = start
            returnasdate = False

        while True:
            if returnasdate is True:
                yield current.date()
            else:
                yield current

            #Update the value
            current += timedelta
