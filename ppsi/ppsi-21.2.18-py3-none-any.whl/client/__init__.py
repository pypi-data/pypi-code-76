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
ppsi client

ppsi client minimally interacts with a running ppsid server
by pushing encoded bytes to a unix socket
'''


import typing
import socket
from psprint import print
from ..common import shell, defined
from .command_codes import req2bytes
from .command_line import cli


def _check_installation() -> None:
    '''
    check if the following dependencies are available:
        * nothing here yet

    '''
    for proc in []:
        if shell.process_comm('command', '-v', proc, fail=False):
            raise FileNotFoundError(f'{proc} not found')


def client_call() -> None:
    '''
    Parse command-line and
    communicate encoded request to unix socket

    Send coded request bytes with kwargs as subcommand bits
    to server socket

    if client was called without arguments,
    show short usage message pointing to -h argument
    '''
    req, kwargs = cli()

    if req is None:
        print('usage: ppsi -h')
        return

    commands: typing.List[bytes] = []
    inst, serial_bytes, serial_len = req2bytes(req, **kwargs)
    if inst is None:
        # bad instruction
        return

    if serial_bytes is not None:
        # pass serialized json object
        commands.append(defined.COMM['ACCEPT'])
        commands.append(serial_len)
        commands.append(serial_bytes)

    commands.append(inst)
    commands.insert(0, defined.COMM['OK'])

    # send command
    response: bytes = defined.COMM['OK']
    try:
        CLIENT = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_STREAM)
        CLIENT.connect(str(defined.SOCK_PATH))
        for cmd in commands:
            if not(response and response == defined.COMM['OK']):
                print(
                    f'SERVER replied {int.from_bytes(response, "big"):0{2}x}',
                    mark='warn'
                )
                break
            CLIENT.send(cmd)
            response = CLIENT.recv(defined.INST_SIZE)
        CLIENT.send(defined.COMM['BYE'])
    except (FileNotFoundError, ConnectionRefusedError):
        # scoket file not found
        print('Confirm that the server is running correctly',
              mark='err')
        return
    except BrokenPipeError:
        if response == defined.COMM['BYE']:
            print("Server Adios", mark='info')
            return
        print('Server Closed unexpectedly')

__all__ = [
    'shell',
    'client_call',
]
