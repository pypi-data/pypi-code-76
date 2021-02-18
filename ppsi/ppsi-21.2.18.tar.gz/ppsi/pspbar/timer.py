#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020-2021 Pradyumna Paranjape
# This file is part of ppsi.
#
# ppsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ppsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ppsi.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Display date-time clock
'''

import typing
import datetime
from .classes import BarSeg


class TimeSeg(BarSeg):
    '''
    Time Segment

    Attributes:
        full = full 24 hour format?
    '''
    full: bool = True

    def call_me(self, _=None) -> typing.Dict[str, str]:
        '''
        create Time summary string

        Args:
            all are ignored

        Returns:
            dict to update ``BarSeg`` properties

        '''
        if self.full:
            return {'magnitude':
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        return {'magnitude':
                datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S")}

    def callback(self, feedback) -> None:
        '''
        Toggle 12/24 hour format
        '''
        self.full = not self.full


TIME = TimeSeg(name="time", symbol='\u23f0')
'''time segment instance'''
