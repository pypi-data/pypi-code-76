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
Watch, log and callback events.

Server tells this script everything that it did.
Some events will trigger function calls:

  * visual feedbacks:

    - volume calls
    - light calls

  * logs:

    - all client comm bytes

'''


import os
import subprocess
from pathlib import Path
from .workspaces import ws_mod
from .volume import vol_feedback
from .light import light_feedback
from . import SWAYROOT


class EventLogger():
    '''
    Event logger container object
    Args:
        wob: subprocess handle for wob pipe
        root: root in which, a hidden log-file '.ppsi.log' is maintained

    '''
    def __init__(self, wob: subprocess.Popen, root: Path = SWAYROOT) -> None:
        self.logfile = Path(os.path.join(root, '.ppsi.log'))
        self.wob = wob
        if self.logfile.exists():
            # old logs will get written to .ppsi.log.last_session
            self.logfile.replace(
                os.path.join(root, '.ppsi.log.last_session')
            )
        self.log = open(self.logfile, 'a')
        self.feedbacks = {
            0x10: (ws_mod, ()),  # workspace changed
            0x60: (vol_feedback, (self.wob, )),  # sound volume
            0x70: (light_feedback, (self.wob, )),  # Screen brightness
        }

    def event_registry(self, *args, **kwargs) -> None:
        '''
        Register events, [callback].

        Callback:
            workspace calls: update workspace manager
            light: visual feedback
            volume: visual feedback

        Args:
            *args: are logged into log-file in the format
                args: arg1
                args: arg2
                ...
            **kwargs: logged into log-file as
                key1: value1
                key2: value2
                ...

        Returns:
            ``None``


        '''
        cmd = kwargs.get('comm')
        for key, val in kwargs.items():
            print(f'{key}: {val:x}', flush=True, file=self.log)
        for val in args:
            print(f'args: {val}', flush=True, file=self.log)
        for code, feedback in self.feedbacks.items():
            if (cmd & 0xF0 == code):
                # strip last hex digit
                feedback[0](*feedback[1])


def open_pipe() -> subprocess.Popen:
    '''
    Open pipe for wob
    '''
    cmd: list = ['wob']
    wobproc = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)
    return wobproc
