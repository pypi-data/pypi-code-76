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
CPU load monitor
'''


import typing
import psutil
from .classes import BarSeg


class LoadSeg(BarSeg):
    '''
    Load Segment
    '''
    def call_me(self, _=None) -> typing.Dict[str, str]:
        '''
        Create CPU load summary string

        Args:
            all are ignored

        Returns:
            dict to update ``BarSeg`` properties

        '''
        color = None
        load_avg = list(map(lambda x: x * 100 / psutil.cpu_count(),
                            psutil.getloadavg()))
        if load_avg[0] > 100:
            color = "#ff5f5fff"
        elif load_avg[0] > 80:
            color = "#ffaf7fff"
        elif load_avg[0] > 60:
            color = "#ffff5fff"
        else:
            return {'vis': False}
        value = "|".join((f'{load:.0f}' for load in load_avg))
        return {'magnitude': value, 'color': color}


LOAD = LoadSeg(name="load", symbol=chr(0x1f3cb), units="%")
'''load monitor segment instance'''
