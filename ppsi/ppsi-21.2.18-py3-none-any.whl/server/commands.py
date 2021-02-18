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
decode commands and subcommands received via unix socket
'''


from .workspaces import ws_mod
from .remote import call_remote
from .passmenu import password
from .wificonnect import refresh_wifi
from .btconnect import connect_bluetooth
from .volume import vol
from .light import light
from .powermenu import system


def empty(**kwargs) -> None:
    '''
    Empty placeholder command

    Args:
        all are ignored

    Returns:
        ``None``
    '''
    print('Empty command called')
    return None


CMD = {
    0x10: ws_mod,
    0x20: call_remote,
    0x30: password,
    0x40: refresh_wifi,
    0x50: connect_bluetooth,
    0x60: vol,
    0x70: light,
    0x80: empty,
    0x90: empty,
    0xA0: empty,
    0xB0: empty,
    0xC0: empty,
    0xD0: empty,
    0xE0: empty,
    0xF0: system,
}
