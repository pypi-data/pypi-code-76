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
bluez api to handle bluetooth connections

calls bluetoothctl for connections
'''

import typing
import re
from launcher_menus import menu
from ..common import shell


def query_known() -> typing.Dict[str, str]:
    '''
    Query bluetoothctl for known bluetooth devices

    Returns:
        names: MAC
    '''
    known_devs = {}
    dev_pat = re.compile(
        r'Device ?((?:.{2}:){5}.{2}) +?(.*)'
    )
    bt_ctl_out = shell.process_comm('bluetoothctl', 'devices',
                                    p_name='remembering')
    for bt_dev in bt_ctl_out.split("\n"):
        device = dev_pat.findall(bt_dev)
        if device:
            known_devs[device[0][1]] = device[0][0]
    return known_devs


def connect_bluetooth(subcmd=None) -> None:
    '''
    ``menu`` offers bluetooth devices to connect.
    connection result is flashed via ``notify``.

    Args:
        all are ignored

    Returns:
        ``None``
    '''
    known_devs = query_known()
    choice = menu(opts=known_devs.keys(), prompt="Connect_to:")
    if choice in known_devs.keys():
        # connect to known device
        response = shell.process_comm(
            'bluetoothctl', 'connect', known_devs[choice],
            p_name='connecting'
        )
        if any(k in response.lower() for k in ('fail', 'error')):
            shell.notify(f'Connection to {choice} failed')
