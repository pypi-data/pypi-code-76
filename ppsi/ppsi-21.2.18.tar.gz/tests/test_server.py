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
test ppsi server

ppsi server
'''


import unittest
from ppsi.common import defined
from ppsi.server.workspaces import (CycleOrder)


class test_server_cycle_order(unittest.TestCase):
    '''
    tests server
    '''
    ws_ord = CycleOrder()

    def test_iadd(self):
        '''
        test method +=
        '''
        # populate
        self.ws_ord += 0
        self.ws_ord += 1
        self.ws_ord += 2
        self.ws_ord += 3
        self.assertEqual(self.ws_ord[-1], 3)
        self.ws_ord += 3
        self.assertEqual(self.ws_ord[-1], 3)
        self.assertEqual(len(self.ws_ord), 4)
        self.ws_ord += 0
        self.assertEqual(len(self.ws_ord), 4)

    def test_reverse(self):
        '''
        test method reverse
        '''
        # populate
        self.ws_ord += 0
        self.ws_ord += 1
        self.ws_ord += 2
        self.ws_ord += 3
        self.ws_ord.reverse()
        self.assertEqual(self.ws_ord[-1], 3)
        self.assertEqual(self.ws_ord[-2], 0)
        self.assertEqual(self.ws_ord[1], 1)
        self.assertEqual(self.ws_ord[0], 2)

    def test_current(self):
        '''
        test method current
        '''
        self.ws_ord += 0
        self.assertEqual(self.ws_ord.current(), 0)

    def test_add(self):
        '''
        test method +
        '''
        self.ws_ord += 0
        self.ws_ord += 1
        self.ws_ord += 2
        self.ws_ord += 3
        self.assertEqual(self.ws_ord + 0, 0)
        self.assertEqual(self.ws_ord + 0, 1)
        self.assertEqual(self.ws_ord + 0, 2)

    def test_sub(self):
        '''
        test method -
        '''
        self.ws_ord += 0
        self.ws_ord += 1
        self.ws_ord += 2
        self.ws_ord += 3
        self.assertEqual(self.ws_ord - 2, 2)
        self.assertEqual(self.ws_ord - 3, 1)
        self.assertEqual(self.ws_ord - 4, 0)
