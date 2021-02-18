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
power command mode api using launcher_menus
'''


from ..common import shell


syscmd = ['suspend', 'poweroff', 'reboot', 'reboot --firmware-setup']


def adjust_lights():
    '''
    set light to 50%
    '''
    shell.process_comm('light', '-S', '50',
                       p_name='adjusting light', fail=False)


def system(subcmd: int = 1):
    '''
    kwargs:
        subcmd: int = command code for systemctl verbs [0, 1, 2, 3]
            0: suspend
            1: poweroff
            2: reboot
            3: bios_reboot [if available, request reboot to firmware bios]

    Returns:
        None

    Handle system power requests
    '''
    subcmd %= len(syscmd)
    adjust_lights()
    verb = syscmd[subcmd - 1].split(" ")
    shell.process_comm('systemctl', *verb, fail=False)
