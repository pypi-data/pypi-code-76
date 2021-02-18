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
test ppsi client

ppsi client
'''


import unittest
import json
from ppsi.common import defined
from ppsi.client.command_codes import (workspaces, comm, blank, vol, light,
                                       system, req2bytes)


class test_client_command_codes(unittest.TestCase):
    '''
    tests client
    '''
    def test_workspaces(self) -> None:
        '''
        test function workspaces
        '''
        subcmd = {
            'reverse': 0x01,
            'oldest': 0x02,
            'latest': 0x03,
            'back': 0x03,
            'default': 0x00,
        }
        for sub, code in subcmd.items():
            byte_code, serial = workspaces(mod=sub)
            self.assertEqual(byte_code, code)
            self.assertEqual(serial, None)

    def test_comm(self) -> None:
        '''
        test function comm
        '''
        subcmd = {
            'quit': 0x0E,
            'exit': 0x0E,
            'reload': 0x0E,
            'default': None,
        }
        for sub, code in subcmd.items():
            byte_code, serial = comm(mod=sub)
            self.assertEqual(byte_code, code)
            self.assertEqual(serial, None)

    def test_blank(self) -> None:
        '''
        test function blank
        '''
        subcmd = {
            'default': None,
        }
        for sub, code in subcmd.items():
            byte_code, serial = blank(mod=sub)
            self.assertEqual(byte_code, code)
            self.assertEqual(serial, None)

    def test_vol(self) -> None:
        '''
        test function volume
        '''
        subcmd = {
            'mute': 0x00,
            '0': 0x00,
            'up': 0x01,
            '+': 0x01,
            'down': 0x02,
            '-': 0x02,
            'default': None,
        }
        test_change = range(0, 100)
        for sub, code in subcmd.items():
            for change in test_change:
                byte_code, serial = vol(mod=sub, change=change)
                self.assertEqual(byte_code, code)
                self.assertEqual(json.loads(serial), {'change': change})

    def test_light(self) -> None:
        '''
        test function light
        '''
        subcmd = {
            'up': 0x01,
            '+': 0x01,
            'down': 0x02,
            '-': 0x02,
        }
        test_change = range(0, 100)
        for sub, code in subcmd.items():
            for change in test_change:
                byte_code, serial = light(mod=sub, change=change)
                self.assertEqual(byte_code, code)
                self.assertEqual(json.loads(serial), {'change': change})

    def test_system(self) -> None:
        '''
        test function light
        '''
        subcmd = {
            'suspend': 0x01,
            'poweroff': 0x02,
            'reboot': 0x03,
            'bios_reboot': 0x04,
        }
        for sub, code in subcmd.items():
            byte_code, serial = system(mod=sub)
            self.assertEqual(byte_code, code)
            self.assertEqual(serial, None)

    def test_req2bytes(self) -> None:
        '''
        test function req2bytes
        '''
        test_inst, test_serial_bytes, test_serial_len_bytes = req2bytes(
            'light', mod='+', change=5
        )
        serial = json.dumps({'change': 5})
        serial_len = len(serial)
        test_serial_len = int(test_serial_len_bytes.decode(defined.CODING))
        test_serial = test_serial_bytes.decode(defined.CODING)
        self.assertEqual(test_inst, 0x71.to_bytes(defined.INST_SIZE, 'big'))
        self.assertEqual(test_serial, serial)
        self.assertEqual(test_serial_len, serial_len)
