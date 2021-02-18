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
pspbar classes


'''


import typing
import sys
import select
from .sway_proto import SwayProtoIn, SwayProtoOut


class BarSeg():
    '''
    Sway Bar Segment object of SBar

    Args:
        name: str: name-handle of the segment
        symbol: str: displayed on bar
        magnitude: str: the string to display
        units: str: suffixed to magnitude
        mem: Any: initial (placeholder) memory to be added to buffer
        ml_tag: str: pango_tag to wrap around magnitude
        call_me: Callable: function that accepts a memory object returns
                (symbol, Magnitude, mem, ?Visible)
        callback: Callable: function called by click on the segment

    Returns:
        ``None``

    '''
    def __init__(self, **kwargs) -> None:
        self.name = None
        self.vis = True
        self.symbol = ''
        self.ml_tag: typing.List[str] = ['', '']
        self.magnitude = ''
        self.units = ''
        self.mem: typing.Any = None
        self.pango: bool = False
        self.__dict__.update(kwargs)
        self.seg_json = SwayProtoIn(name=self.name,
                                    full_text=self.full_text)

    def call_me(self, _=None) -> typing.Dict[str, str]:
        '''
        Args:
            all are ignored

        Dumb call
        '''
        return {}

    def callback(self, _) -> None:
        '''
        Args:
            all are ignored

        void callback
        '''
        return None

    @property
    def full_text(self):
        '''
        Create full_text from symbol, ml_tag, magnitude, units
        '''
        if self.vis:
            return ' '.join(
                [self.symbol,
                 self.ml_tag[0], self.magnitude, self.ml_tag[1],
                 self.units]
            )
        else:
            return None

    @full_text.deleter
    def full_text(self):
        '''
        delete magnitude
        '''
        self.magnitude = ''
        self.ml_tag = ['', '']

    def set_proto(self, **kwargs) -> None:
        '''
        Set protocol keys

        Args:
            **kwargs: passed on to update function of ``SwayProtoIn``

        Returns:
            ``None``

        '''
        self.seg_json.update(**kwargs)

    def update(self, custom: typing.Callable = None, **kwargs) -> None:
        '''
        Update magnitude and symbol

        Args:
            custom: function that updates the segment
            **kwargs:
                symbol: to update
                magnitude: to update
                mem: to update
                ml_tag: pango tag to decorate
                vis: (bool) visibility
                other kwargs are passed on to ``SwayProtoIn``

        '''
        kwargs = (custom or self.call_me)(self.mem)
        for key in 'symbol', 'magnitude', 'mem', 'ml_tag', 'vis':
            if key in kwargs:
                setattr(self, key, kwargs[key])
                del kwargs[key]
        self.seg_json.update(**kwargs, full_text=self.full_text)
        # print(self.seg_json)


class SBar():
    '''
    Sway bar wrapper class
    Attributes:
        bar_str: final json serialized bar_string that is pushed to swaybar
        bar_segs: segments present in instance
        quick_segments: list of segments that update `quickly`
        slow_segments: list of segments that update `slowly`
        static_segments: list of segments that don't update
    '''
    def __init__(self) -> None:
        self.bar_str = ''
        self.bar_segs = []
        self.quick_segs = []
        self.slow_segs = []
        self.static_segs = []

    def add_segs(self, segment: BarSeg,
                 interval: int = 1, position: int = None) -> None:
        '''
        Add segment to bar

        Args:
            position: Position of segment from edge [end]
            interval: Interval of update.

        Numerical code for interval:
            Beginning: 0,
            frequently: 1,
            intermittently: 2.

        Returns:
            ``None``

        '''
        self.bar_segs.insert(position, segment)

        if interval == 1:
            self.quick_segs.append(segment)
        elif interval == 2:
            self.slow_segs.append(segment)
        else:
            self.static_segs.append(segment)

    def _slow_tick(self) -> None:
        '''
        Update slow-updating segments
        '''
        for seg in self.slow_segs:
            seg.update()

    def _quick_tick(self) -> None:
        '''
        Update fast-updating widgets
        '''
        for seg in self.quick_segs:
            seg.update()

    def _static_vals(self) -> None:
        '''
        Define static segments
        '''
        for seg in self.static_segs:
            seg.update()

    def _update_str(self) -> None:
        '''
        Update bar string
        '''
        self.bar_str = f", [{self.bar_str}]"
        self.bar_str = ", [" + (
            ','.join(
                reversed(
                    [str(seg.seg_json)
                     for seg in filter(lambda x: x.vis, self.bar_segs)]
                )
            )
        ) + "]"

    def loop(self, period: int = 1, multi: int = 1) -> None:
        '''
        The bar-update loop
        Args:
            period: Period between two updates in seconds.
            multi: Multiplier to period that gives slow update period.

        Returns:
            ``None``

        '''
        self._static_vals()
        long_per = 0
        while True:
            self._quick_tick()
            if long_per == 0:
                self._slow_tick()
            self._update_str()
            print(self.bar_str, flush=True)
            long_per = (long_per + period) % multi
            # sleep(period)
            trig, _, _ = select.select([sys.stdin], [], [], period)
            if trig:
                feedback = sys.stdin.readline().rstrip("\n")
                sway_comm = SwayProtoOut(feedback)
                for seg in filter(lambda x: x.name == sway_comm.name,
                                  self.bar_segs):
                    seg.callback(sway_comm)
