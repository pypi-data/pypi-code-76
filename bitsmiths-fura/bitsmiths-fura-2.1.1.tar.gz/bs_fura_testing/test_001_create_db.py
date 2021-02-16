#!/usr/bin/env python

# **************************************************************************** #
#                           This file is part of:                              #
#                                BITSMITHS                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/bitsmiths                             #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #

import glob
import os
import unittest

from bs_lib_testing import helper


DEBUG   = False
VERBOSE = False


def setUpModule():
    helper._data['debug']      = DEBUG
    helper._data['verbose']    = VERBOSE
    helper.init_environ('fura')


def tearDownModule():
    pass


class TestFuraCreateDB(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.data  = helper._data
        cls.usrId = '[TestFuraCreateDB]'


    @classmethod
    def tearDownClass(cls):
        pass


    def test_001_drop_create_database(self):
        if DEBUG: return

        helper.create_database(['fura', 'audit', 'loco'])


    def test_002_connect_to_database(self):
        if DEBUG: return

        helper.connect_to_database()


    def test_003_create_tables(self):
        if DEBUG: return

        for product in [ 'triceraclops', 'loco' ]:
            pth = os.path.join('..', '..', '..', product, 'mettledb', 'sqldef', 'postgresql')

            self.assertEqual(True, os.path.exists(pth))

            for ext in ['*.table', '*.constraint', '*.index']:
                sql_list = glob.glob(os.path.join(pth, ext))

                for sql_file in sql_list:
                    sql_cmds = helper.get_sql_commands_from_file(self, sql_file, mettle_gen=True)

                    for cmd in sql_cmds:
                        helper.sql_run(cmd)

            helper.sql_commit()

            sql_file = os.path.join('..', '..', '..', product, 'sql', 'initdb_postgresql.sql')

            if os.path.exists(sql_file):
                sql_cmds = helper.get_sql_commands_from_file(self, sql_file, mettle_gen=False)

                for cmd in sql_cmds:
                    helper.sql_run(cmd)

                helper.sql_commit()


        pth = os.path.join('..', '..', 'mettledb', 'sqldef', 'postgresql')

        self.assertEqual(True, os.path.exists(pth))

        for ext in ['*.table', '*.constraint', '*.index']:
            sql_list = glob.glob(os.path.join(pth, ext))

            for sql_file in sql_list:
                sql_cmds = helper.get_sql_commands_from_file(self, sql_file, mettle_gen=True)

                for cmd in sql_cmds:
                    helper.sql_run(cmd)

        helper.sql_commit()


    def test_004_insert_static_data(self):
        if DEBUG: return

        pth  = os.path.join('..', '..', 'sql')

        self.assertEqual(True, os.path.exists(pth))

        for ext in ['*.sql']:
            sql_list = glob.glob(os.path.join(pth, ext))

            for sql_file in sql_list:
                sql_cmds = helper.get_sql_commands_from_file(self, sql_file, mettle_gen=False)

                for cmd in sql_cmds:
                    helper.sql_run(cmd)

        helper.sql_commit()


    def test_005_InsertTestData(self):
        if DEBUG: return

        helper.sql_run("insert into fura.role values (1, 'test', 'Test role', 'A', 1, 10, '%s', current_timestamp)" % self.usrId) # noqa
        helper.sql_run("insert into fura.usr values (1, 'test', 'test', 'A', 'Test', 'Test', null, current_date, null, null, null, null, null, '%s', current_timestamp, 'sys', false, false, false, false, false, false, false)" % self.usrId) # noqa
        helper.sql_commit()


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
