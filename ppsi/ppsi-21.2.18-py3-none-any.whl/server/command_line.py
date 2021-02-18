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
'''
command-line parser for ppsid server

parse command line to
    interpret server configuration, environment and
    start ppsid server
'''


from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from .read_config import read_config


def cli():
    '''
    server command line parser
    '''
    swayroot, config = None, None
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-f', '--conf-file', type=str, help='config yaml file',
        default=None)
    parser.add_argument(
        '-r', '--sway-root', type=str, help='root for sway files',
        default=None
    )
    args = parser.parse_args()
    if args.sway_root is not None or args.conf_file is not None:
        swayroot, config = read_config(custom_conf=args.conf_file,
                                       swayroot=args.sway_root)
    del args.sway_root
    del args.conf_file
    return swayroot, config, vars(args)
