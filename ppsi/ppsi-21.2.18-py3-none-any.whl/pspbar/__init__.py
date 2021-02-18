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
Personal Swaybar in Python

Bar that follows swaybar-protocol with an interface to ``ppsi`` functions.

Defines:

  * An interface to input and output data according to swaybar protocol.
  * Simplified Generic segment-object ``BarSeg`` to feed segments.
  * ``SBar`` bar manager to update various segments at different intervals.

'''


import sys
import datetime
import time
import warnings
import json
from ..common import shell
from .command_line import cli
from .classes import SBar, BarSeg
from .battery import BATTERY
from .timer import TIME
from .cpu import CPU
from .ram import RAM
from .network import IP_ADDR, NETSPEED
from .temperature import TEMPERATURE
from .uname import OSNAME
from .load_average import LOAD


def _check_installation() -> None:
    '''
    Check if the following dependencies are available:
        * nothing here yet

    '''
    for proc in []:
        if shell.process_comm('command', '-v', proc, fail=False):
            raise FileNotFoundError(f'{proc} not found')


def pspbar():
    '''
    Fetch parameters from cli and launch pspbar

    Returns:
        ``None``

    Main Routine
    '''
    period, multi = cli()
    if 'psutil' not in sys.modules:
        while True:
            # basic output
            print('<span foreground=\\"#ff7f7fff\\"> Install psutil',
                  'meanwhile, falling back to basic:\t',
                  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  '</span>', flush=True)
            time.sleep(1)
    else:
        warnings.filterwarnings('ignore')
        topbar = SBar()
        NETSPEED.mem = [period * multi, 0, 0]
        topbar.add_segs(segment=TIME, position=0, interval=1)
        topbar.add_segs(segment=BATTERY, position=1, interval=2)
        topbar.add_segs(segment=CPU, position=2, interval=1)
        topbar.add_segs(segment=TEMPERATURE, position=3, interval=2)
        topbar.add_segs(segment=RAM, position=4, interval=1)
        topbar.add_segs(segment=IP_ADDR, position=5, interval=0)
        topbar.add_segs(segment=NETSPEED, position=6, interval=2)
        topbar.add_segs(segment=OSNAME, position=7, interval=0)
        topbar.add_segs(segment=LOAD, position=8, interval=2)
        header = {'version': 1, "click_events": True}
        print(json.dumps(header), "[", "[]", sep="\n")
        topbar.loop(period=period, multi=multi)


__all__ = [
    'pspbar',
    'BarSeg',
    'SBar',
]
