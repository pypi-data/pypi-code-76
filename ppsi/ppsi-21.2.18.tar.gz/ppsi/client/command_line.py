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
command-line parser for ppsi client

parse command line to interpret request and corresponding subcommands
'''


import typing
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import argcomplete


def cli() -> typing.Tuple[str, dict]:
    '''
    Client command line parser

    '''
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()

    _ = subparsers.add_parser(name='help', help='show this help')
    remote = subparsers.add_parser(name='remote', help='connect to remote')
    passwd = subparsers.add_parser(name='pass', help='get passwords')
    wifi = subparsers.add_parser(name='wifi', help='reconnect wifi')
    bluetooth = subparsers.add_parser(name='bluetooth',
                                      help='reconnect bluetooth')
    remote.set_defaults(req='remote')
    passwd.set_defaults(req='pass')
    wifi.set_defaults(req='wifi')
    bluetooth.set_defaults(req='bluetooth')

    workspace = subparsers.add_parser(name='workspace', help='set keybindings')
    workspace.set_defaults(req='workspace')
    workspace.add_argument('mod', type=str, nargs='?', default='update',
                           choices=['update', 'reverse', 'oldest', 'latest'])

    ppsi_comm = subparsers.add_parser(name='comm', help='ppsi instructions')
    ppsi_comm.set_defaults(req='comm')
    ppsi_comm.add_argument('mod', type=str, choices=['reload', 'quit'])

    vol = subparsers.add_parser(name='vol', help='change volume')
    vol.set_defaults(req='vol')
    vol.add_argument('mod', type=str, choices=['up', 'down', 'mute',
                                               '+', '-', '0'])
    vol.add_argument('change', type=int, default=2, nargs="?")

    light = subparsers.add_parser(name='light', help='change light')
    light.set_defaults(req='light')
    light.add_argument('mod', type=str, choices=['up', 'down', 'mute',
                                                 '+', '-', '0'])
    light.add_argument('change', type=int, default=2, nargs='?')

    system = subparsers.add_parser(name='system', help='system utils')
    system.add_argument('mod', choices=['suspend', 'poweroff',
                                        'reboot', 'bios_reboot'])
    system.set_defaults(req='system')
    argcomplete.autocomplete(parser)
    kwargs = vars(parser.parse_args())
    req: str = kwargs.get('req', 'help')
    if req == 'help':
        parser.print_help()
        req = ''
    if 'req' in kwargs:
        del kwargs['req']
    return req, kwargs
