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
PPSI client pre-processing

process command/sub-command to be communicated by client to socket
'''


import typing
import json
from ..common import defined


def workspaces(mod: str = None, **kwargs) -> typing.Tuple[int, str]:
    '''
    Workspace actions.

    Args:
        mod: mode of workspace cycle {reverse,oldest,latest,back,None}:
            `reverse`: reverse the order of workspace cycle.
            `oldest`: switch to the oldest workspace.
            `latest`: switch to the satest workspace (back-and-forth).
            `back`: =latest.
            ``None``: Update keybindings, manager about workspace switch.
        **kwargs: all are ignored

    Returns:
        tuple(code of mod, ``None``)
    '''
    subcmd = {
        'reverse': 0x01,
        'oldest': 0x02,
        'latest': 0x03,
        'back': 0x03
    }.get(mod, 0x00)
    return subcmd, None


def comm(mod: str = None, **kwargs) -> typing.Tuple[int, str]:
    '''
    Communication instructions to ppsid server
    'reload' is Not working yet.

    Args:
        mod: mode of ppsid call {reload,quit,exit}:
            `reload`: reload ppsid server.
            `quit`: quit ppsid server.
            `exit`: =quit.
        **kwargs: all are ignored

    Returns:
        tuple(code of mod, ``None``)
    '''
    mod = kwargs.get('mod')
    mod_menu = {
        'quit': 0x0E,
        'exit': 0x0E,
        'reload': 0x0E,
    }
    subcmd = mod_menu.get(mod)
    return subcmd, None


def blank(**kwargs) -> typing.Tuple[int, str]:
    '''
    Blank placeholder.

    Args:
        all are ignored

    Returns:
        tuple(0, ``None``)

    '''
    # abort
    return 0x00, None


def vol(mod: str = None, **kwargs) -> typing.Tuple[int, str]:
    '''
    Volume action.

    Args:
        mod: mode of volume command {up,down,mute,+,-,0}:
            `up`: increase volume.
            `down`: decrease volume.
            `mute`: mute speaker output channel.
            `+`: =up.
            `-`: =down.
            `0`: =mute.
        **kwargs: all are json serialized and returned
            change: % change in volume requested

    Returns:
        tuple(code of mod, json(kwargs))

    '''
    mod_menu = {
        'mute': 0x00,
        '0': 0x00,
        'up': 0x01,
        '+': 0x01,
        'down': 0x02,
        '-': 0x02,
    }
    subcmd = mod_menu.get(mod)
    return subcmd, json.dumps(kwargs)


def light(mod: str = None, **kwargs) -> typing.Tuple[int, str]:
    '''
    Brightness actions.

    Args:
        mod: mode of light command {up,down,+,-}:
            `up`: increase brightness.
            `down`: decrease brightness.
            `+`: =up.
            `-`: =down.
        **kwargs: all are json serialized and returned.
            change: % change in brightness requested.

    Returns:
        tuple(code of mod, json(kwargs))

    '''
    mod_menu = {
        'up': 0x01,
        '+': 0x01,
        'down': 0x02,
        '-': 0x02,
    }
    subcmd = mod_menu.get(mod)
    return subcmd, json.dumps(kwargs)


def system(mod: str = None, **kwargs) -> typing.Tuple[int, str]:
    '''
    Systemctl instructions.

    Args:
        mod: mode of system call {suspend,poweroff,reboot,bios_reboot}:
            `suspend`: suspend system.
            `poweroff`: poweroff system.
            `reboot`: reboot system.
            `bios_reboot`: reboot system to open in bios [if supported].
        **kwargs: all are ignored

    Returns:
        typing.Tuple[code of mod, ``None``]

    '''
    mod_menu = {
        'suspend': 0x01,
        'poweroff': 0x02,
        'reboot': 0x03,
        'bios_reboot': 0x04,
    }
    sub_byte = mod_menu.get(mod)
    return sub_byte, None


CMD: typing.Dict[str, int] = {
    "comm": 0x00,
    "workspace": 0x10,
    "remote": 0x20,
    "pass": 0x30,
    "wifi": 0x40,
    "bluetooth": 0x50,
    "vol": 0x60,
    "light": 0x70,
    "system": 0xF0,
}


SUB_ARGS: typing.Dict[int, typing.Callable] = {
    0x00: comm,
    0x10: workspaces,
    0x20: blank,
    0x30: blank,
    0x40: blank,
    0x50: blank,
    0x60: vol,
    0x70: light,
    0x80: blank,
    0x90: blank,
    0xA0: blank,
    0xB0: blank,
    0xC0: blank,
    0xD0: blank,
    0xE0: blank,
    0xF0: system,
}


def req2bytes(req: str, **kwargs) -> typing.Tuple[bytes, bytes, bytes]:
    '''
    Convert request to encoded instruction bytes and
    byte-encoded serialized input data for the instruction.

    Args:
        req: request string from command-line
        **kwargs: passed to subcommand coding function for serialization

    Returns:
        tuple:
            instruction byte (bytes encoded) or ``None``,
            json-serialized ``**kwargs`` (bytes encoded) or ``None``,
            length of serial_bytes (bytes encoded) or ``None``

    '''
    serial_bytes, serial_len = None, None
    base = CMD.get(req)
    if base is None:
        # bad request
        return None, None, None
    sub_byte, serial = SUB_ARGS[base](**kwargs)
    if sub_byte is None:
        # bad sub-argument
        return None, None, None

    inst: bytes = (base + sub_byte).to_bytes(defined.INST_SIZE, 'big')

    if serial is not None:
        serial_bytes: bytes = serial.encode(defined.CODING)
        serial_len: bytes = str(len(serial_bytes)).encode(defined.CODING)
        serial_len += b' ' * (defined.HEAD_SIZE - len(serial_len))

    return inst, serial_bytes, serial_len
