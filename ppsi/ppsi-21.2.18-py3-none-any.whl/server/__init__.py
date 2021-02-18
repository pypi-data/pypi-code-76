#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-
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
ppsi server

Listen to and execute commands sent by ppsi client
'''


import daemon
from ..common import shell
from .read_config import read_config  # default configs


SWAYROOT, CONFIG = read_config(None, None)


def _check_instalaltion():
    '''
    check if following dependencies are available
     * swaymsg: sway
     * nmcli: NetworkManager
     * bluetoothctl: bluez
     * pacmd: pulseaudio
     * pactl: pulseaudio
     * light: light
     * wob: wob
     * pass: password manager
     * wl-copy: wayland copy xclip
     * systemctl: systemctl
    '''
    for proc in [
            'swaymsg',  # sway
            'nmcli',  # NetworkManager
            'bluetoothctl',  # bluez
            'pacmd',  # pulseaudio
            'pactl',  # pulseaudio
            'light',  # light
            'wob',  # wob
            'pass',  # password manager
            'wl-copy'  # wayland copy xclip
            'systemctl',  # systemctl
    ]:
        if shell.process_comm('command', '-v', proc, fail=False):
            raise FileNotFoundError(f'{proc} not found')


def _server_call(**kwargs) -> None:
    '''
    server_call
    '''
    from .command_line import cli
    newroot, newconfig, kwargs = cli()
    if newroot is not None:
        globals()['SWAYROOT'] = newroot
    if newconfig is not None:
        globals()['CONFIG'] = newconfig

    from .server import start_srv
    start_srv(**kwargs)

def server_call(debug: bool = False, **kwargs) -> None:
    '''
    Start ppsid server

    Args:
        debug: do not daemonize server, output gets printed to STDOUT
        **kwargs: passed to ``ppsi.server.start_srv``

    '''
    if debug:
        with daemon.DaemonContext():
            _server_call()
    else:
        _server_call()

__all__ = [
    'CONFIG',
    'SWAYROOT'
    'server_call'
]
