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
Wifi connection menu

Refresh available wifi APs and offer to connect to one
If known, connect. If unknown, ask for password

'''


import typing
import re
from launcher_menus.themes import password_prompt, menu
from ..common import shell


def query_known() -> typing.List[str]:
    '''
    Query nmcli for known wifi APs

    Returns:
        Known Wifi AP names
    '''
    known_aps = []
    conn_pat = re.compile(
        r'(.+?) +?\w{8}-\w{4}-\w{4}-\w{4}-\w{12}  wifi +'
    )
    stdout = shell.process_comm('nmcli', 'connection', 'show',
                                p_name='remembering')
    for connection in stdout.split("\n"):
        wifi_conn = conn_pat.findall(connection)
        if wifi_conn:
            known_aps += wifi_conn
    return known_aps


def query_available() -> typing.List[str]:
    '''
    Query nmcli for available wifi APs

    Returns:
        Available Wifi AP names
    '''
    available_aps = []
    info_pat = re.compile(
        r'\*? +(?:\w{2}:){5}\w{2} +(.+?) +\w+? +\d+ +.+? .+? +(\d+?) +'
    )
    stdout = shell.process_comm(
        'nmcli', 'device', 'wifi', 'list', '--rescan', 'yes',
        p_name='discovering'
    )
    for info_str in stdout.split("\n"):
        grab = info_pat.findall(info_str)
        if grab:
            available_aps += grab
    return available_aps


def refresh_wifi(subcmd=None) -> None:
    '''
    Offer a available wifi APs to connect
    if the entered wifi ap is not known, request password

    connection success is flashed via ``notify``

    Args:
        all are ignored

    Returns:
        ``None``

    '''
    known_aps = query_known()
    available_aps = query_available()
    if not available_aps:
        shell.notify('No wifi network available', timeout=0)
        return
    choice = menu(
        opts=[':'.join(info)
              for info in sorted(
                      available_aps,
                      key=(lambda x: int(x[-1])
                           ),
                      reverse=True)],
        prompt="connect to"
    )
    if choice is None:
        return
    choice, *_ = choice.split(":")
    cmd = ['nmcli', 'device', 'wifi', 'connect', choice.replace(' ', "\\ ")]
    if choice not in known_aps:
        wifi_pass = password_prompt( opts=[], fail=True)
        cmd += ['password', wifi_pass.replace(' ', "\\ ")]
    stdout = shell.process_comm(*cmd, p_name='connecting')
    if stdout is None or 'error' in stdout.lower():
        shell.notify(f'Error connecting: {stdout}')
    else:
        shell.notify(f'Connected to {choice}')
