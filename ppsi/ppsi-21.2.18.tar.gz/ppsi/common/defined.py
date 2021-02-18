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
Global definitions for ppsi socket that are inhereted by both
`ppsid` server and `ppsi` client
'''


import os
from pathlib import Path

# location of socket in a RUNTIME DIRRECTORY
RUN_LOC = [
    os.environ.get('XDG_RUNTIME_DIR'),  # Good practice
    os.path.join('/run/user', os.environ.get('UID', 'current_user')),  # hard
    os.path.join(os.environ.get('HOME'), '.runtime')  # Alas!
]
'''
Default locations of runtime directory:
    * From environment {XDG_RUNTIME_DIR} ELSE
    * as hardcoded /run/user/$UID ELSE
    * as ${HOME}/.runtime
'''

for location in RUN_LOC:
    if location is not None and Path(location).is_dir():
        SOCK_PARENT = Path(location).joinpath(location, 'sway')
        if not SOCK_PARENT.is_dir():
            SOCK_PARENT.mkdir()
        SOCK_PATH: Path = SOCK_PARENT.joinpath('ppsi.sock')
        break

INST_SIZE = 0x1  # 1 byte(s) = 16 communications + 15 commands * 16 subcommands
'''
length (in bytes) of instructions
'''

HEAD_SIZE = 64  # Seriously! this is 2 ** 64 = 16 exabytes!
'''
length (in bytes) of header (that tells the server how many bytes to recv)
'''

CODING = 'utf-8'
'''
character encoding used by server and client
'''

COMM = {
    'OK':     0x00.to_bytes(1, 'big'),  # OK
    'ACCEPT': 0x0A.to_bytes(1, 'big'),  # Please Accept JSON of kwargs
    'BYE':    0x0B.to_bytes(1, 'big'),  # BYE BYE
    'EXIT':   0x0E.to_bytes(1, 'big'),  # Request Exit server
    'FAULT':  0x0F.to_bytes(1, 'big'),  # Fault (ERROR)
}
'''
server-client communication commands 0x00 to 0x0F
'''
