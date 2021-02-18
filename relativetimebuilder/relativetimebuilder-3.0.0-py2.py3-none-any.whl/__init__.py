# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import dateutil.relativedelta

from aniso8601.builders import BaseTimeBuilder, DateTuple, TupleBuilder
from aniso8601.builders.python import (FractionalComponent, PythonTimeBuilder,
                                       MICROSECONDS_PER_SECOND,
                                       MICROSECONDS_PER_MINUTE,
                                       MICROSECONDS_PER_HOUR,
                                       MICROSECONDS_PER_DAY,
                                       MICROSECONDS_PER_WEEK,
                                       MICROSECONDS_PER_MONTH,
                                       MICROSECONDS_PER_YEAR)
from relativetimebuilder.version import __version__

class RelativeValueError(ValueError):
    """Raised when an invalid value is given for calendar level accuracy."""

class RelativeTimeBuilder(PythonTimeBuilder):
    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):
        years = 0
        months = 0
        days = 0
        weeks = 0
        hours = 0
        minutes = 0
        seconds = 0
        microseconds = 0

        PnY, PnM, PnW, PnD, TnH, TnM, TnS = BaseTimeBuilder.range_check_duration(PnY, PnM, PnW, PnD, TnH, TnM, TnS, rangedict=PythonTimeBuilder.DURATION_RANGE_DICT)

        if type(PnY) is FractionalComponent or type(PnM) is FractionalComponent:
            #https://github.com/dateutil/dateutil/issues/40
            raise RelativeValueError('Fractional months and years are not '
                                     'defined for relative durations.')

        if PnY is not None:
            years = PnY

        if PnM is not None:
            months = PnM

        if PnW is not None:
            if type(PnW) is FractionalComponent:
                weeks = PnW.principal
                microseconds = PnW.microsecondremainder
            else:
                weeks = PnW

        if PnD is not None:
            if type(PnD) is FractionalComponent:
                days = PnD.principal
                microseconds = PnD.microsecondremainder
            else:
                days = PnD

        if TnH is not None:
            if type(TnH) is FractionalComponent:
                hours = TnH.principal
                microseconds = TnH.microsecondremainder
            else:
                hours = TnH

        if TnM is not None:
            if type(TnM) is FractionalComponent:
                minutes = TnM.principal
                microseconds = TnM.microsecondremainder
            else:
                minutes = TnM

        if TnS is not None:
            if type(TnS) is FractionalComponent:
                seconds = TnS.principal
                microseconds = TnS.microsecondremainder
            else:
                seconds = TnS

        years, months, weeks, days, hours, minutes, seconds, microseconds = PythonTimeBuilder._distribute_microseconds(microseconds, (years, months, weeks, days, hours, minutes, seconds), (MICROSECONDS_PER_YEAR, MICROSECONDS_PER_MONTH, MICROSECONDS_PER_WEEK, MICROSECONDS_PER_DAY, MICROSECONDS_PER_HOUR, MICROSECONDS_PER_MINUTE, MICROSECONDS_PER_SECOND))

        return dateutil.relativedelta.relativedelta(years=years,
                                                    months=months,
                                                    weeks=weeks,
                                                    days=days,
                                                    hours=hours,
                                                    minutes=minutes,
                                                    seconds=seconds,
                                                    microseconds=microseconds)

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
                            or durationobject.microseconds != 0)

        if end is not None:
            #<duration>/<end>
            endobject = cls._build_object(end)

            #Range check
            if type(end) is DateTuple:
                enddatetime = cls.build_datetime(end, TupleBuilder.build_time())

                if datetimerequired is True:
                    #<end> is a date, and <duration> requires datetime resolution
                    return (endobject,
                            cls.build_datetime(end, TupleBuilder.build_time())
                            - durationobject)

            return (endobject,
                    endobject
                    - durationobject)

        #<start>/<duration>
        startobject = cls._build_object(start)

        #Range check
        if type(start) is DateTuple:
            startdatetime = cls.build_datetime(start, TupleBuilder.build_time())

            if datetimerequired is True:
                #<start> is a date, and <duration> requires datetime resolution
                return (startobject,
                        cls.build_datetime(start, TupleBuilder.build_time())
                        + durationobject)

        return (startobject,
                startobject
                + durationobject)
