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

import unittest

from bs_lib.auto_transaction import AutoTransaction

from bs_lib_testing import helper

from bs_fura.dao            import Dao
from bs_fura.access         import Access
from bs_fura.xfura          import xFura
from bs_fura.user_login     import UserLogin

from bs_fura.db.tables.usr_auth import tUsrAuth

from bs_fura.braze import ResetMethod_Couplet


DEBUG   = False
VERBOSE = True
DB_DAO  = 'postgresql'


def setUpModule():
    helper._data['debug']      = DEBUG
    helper._data['verbose']    = VERBOSE
    helper.init_environ('fura')
    helper.init_pod()
    helper._data['fdao'] = Dao(helper._data['pod'], DB_DAO)


def tearDownModule():
    pass


class TestFuraLibrary(unittest.TestCase):

    TEST_PASSWD = 'h3ll0-World@Q#W'


    @classmethod
    def setUpClass(cls):
        cls.data   = helper._data
        cls.usr_id = '[TestFuraLibrary]'
        cls.fdao   = helper._data['fdao']
        cls.pod    = helper._data['pod']


    @classmethod
    def tearDownClass(cls):
        pass


    def test_011_access_test_super_user(self):
        if DEBUG: return

        src = __name__

        helper.sql_run("delete from fura.ada")
        helper.sql_run("delete from fura.aga")
        helper.sql_commit()

        with AutoTransaction(self.pod) as at:
            with Access(self.fdao, 'FURA', 'admin', src) as ac:
                self.assertTrue(ac.ok())
                self.assertTrue(ac.access('fura.cfg.create'))
                self.assertTrue(ac.access('fura.site.delete'))
                self.assertTrue(ac.access('fura.role.update'))

                self.assertTrue(ac.ok())

            at.commit()

        res = helper.sql_fetch("select * from fura.aga")

        self.assertIsNotNone(res)
        self.assertEqual(3, len(res))


    def test_012_access_test_test_user(self):
        if DEBUG: return

        src = __name__

        helper.sql_run("delete from fura.rolefuncrel where site_id = 1 and role_id = 'test'")
        helper.sql_run("delete from fura.ada")
        helper.sql_run("delete from fura.aga")
        helper.sql_commit()

        with AutoTransaction(self.pod) as at:
            with Access(self.fdao, 'FURA', 'test', src) as ac:
                self.assertTrue(ac.ok())
                self.assertFalse(ac.access('fura.cfg.create'))
                self.assertFalse(ac.access('fura.site.delete'))
                self.assertFalse(ac.access('fura.role.update'))

                self.assertFalse(ac.ok())

            at.commit()

        res = helper.sql_fetch("select * from fura.ada")

        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))

        helper.sql_run("delete from fura.ada")
        helper.sql_run("delete from fura.aga")

        helper.sql_commit()

        with AutoTransaction(self.pod) as at:
            with Access(self.fdao, 'FURA', 'test', src) as ac:
                self.assertTrue(ac.ok())
                self.assertFalse(ac.access('fura.cfg.create',  ignore_ada = True))
                self.assertFalse(ac.access('fura.site.delete', ignore_ada = True))
                self.assertFalse(ac.access('fura.role.super',  ignore_ada = True))

                self.assertFalse(ac.ok())

            at.commit()

        res = helper.sql_fetch("select * from fura.ada")

        self.assertIsNotNone(res)
        self.assertEqual(3, len(res))

        helper.sql_run("delete from fura.ada")
        helper.sql_run("delete from fura.aga")
        helper.sql_run("insert into fura.rolefuncrel values(1, 'test', 'fura.cfg.create', '%s', current_timestamp)" % self.usr_id)  # noqa
        helper.sql_run("insert into fura.rolefuncrel values(1, 'test', 'fura.cfg.update', '%s', current_timestamp)" % self.usr_id)  # noqa

        helper.sql_commit()

        with AutoTransaction(self.pod) as at:
            with Access(self.fdao, 'FURA', 'test', src) as ac:
                self.assertTrue(ac.ok())
                self.assertTrue(ac.access('fura.cfg.create'))
                self.assertTrue(ac.access('fura.cfg.update'))
                self.assertFalse(ac.access('fura.site.delete'))
                self.assertFalse(ac.access('fura.role.super', ignore_ada = True))

                self.assertFalse(ac.ok())

            at.commit()

        resd = helper.sql_fetch("select * from fura.ada")
        resg = helper.sql_fetch("select * from fura.aga")

        self.assertIsNotNone(resd)
        self.assertIsNotNone(resg)
        self.assertEqual(2, len(resd))
        self.assertEqual(2, len(resg))

        with self.assertRaises(xFura):
            with Access(self.fdao, 'FURA', 'test', src) as ac:
                ac.required('fura.site.delete')


    def test_021_usr_login_test(self):
        if DEBUG: return

        helper.sql_run("delete from fura.ula where site_id = 1")
        helper.sql_run("delete from fura.usrauth where usr_id = 'bsadmin' and site_id = 1")
        helper.sql_run("delete from fura.usrotp where usr_id = 'bsadmin' and site_id = 1")
        helper.sql_run("delete from fura.usr where id = 'bsadmin' and site_id = 1")
        helper.sql_run("insert into fura.usr values(1, 'bsadmin', 'admin', 'A', null, null, null, null, null, null, null, null, null, '%s', current_timestamp, 'sys', false, false, false, false, false, false, false)" % self.usr_id) # noqa
        helper.sql_commit()

        from bs_triceraclops.audit  import Audit as TriAudit

        tri_audit = TriAudit(self.pod.dbcon, DB_DAO)

        try:

            with UserLogin(self.fdao, 'FURA') as ul:
                ul.set_auth_data(tri_audit,
                                 'bsadmin',
                                 tUsrAuth.AuthType_Couplet.key_password,
                                 self.TEST_PASSWD,
                                 None,
                                 None)

            with UserLogin(self.fdao, 'FURA') as ul:
                ul.login('bsadmin', tUsrAuth.AuthType_Couplet.key_password, self.TEST_PASSWD)
        finally:
            helper.sql_commit()

        res = helper.sql_fetch("select * from fura.ula where site_id = 1 and usr_id = 'bsadmin'")

        self.assertEqual(2,  len(res))
        self.assertEqual('S', res[0]['state'])
        self.assertEqual('S', res[1]['state'])


    def test_022_usr_reset_auth(self):
        if DEBUG: return

        helper.sql_run("delete from fura.usrauth where usr_id = 'bsadmin' and site_id = 1")
        helper.sql_commit()

        from bs_triceraclops.audit  import Audit as TriAudit

        tri_audit = TriAudit(self.pod.dbcon, DB_DAO)

        try:
            with UserLogin(self.fdao, 'FURA') as ul:
                tok = ul.reset_auth('bsadmin',
                                    tUsrAuth.AuthType_Couplet.key_password,
                                    ResetMethod_Couplet.key_email,
                                    None)

                helper.sql_commit()

            self.assertIsNotNone(tok)

            res = helper.sql_fetch("select * from fura.usrotp where site_id=1 and usr_id='bsadmin' and target='auth-reset'",
                                   one=True)

            self.assertIsNotNone(res)
            self.assertEqual(res['otp'],        tok)
            self.assertNotEqual(res['expire'],  None)
            self.assertEqual(res['used'],       False)
            self.assertEqual(res['fail_cnt'],   0)

            with UserLogin(self.fdao, 'FURA') as ul:
                ul.set_auth_data(tri_audit,
                                 'bsadmin',
                                 tUsrAuth.AuthType_Couplet.key_password,
                                 self.TEST_PASSWD,
                                 tok,
                                 ResetMethod_Couplet.key_email)

            res = helper.sql_fetch("select * from fura.usrauth where site_id=1 and usr_id='bsadmin' and auth_type='%s'" % (
                tUsrAuth.AuthType_Couplet.key_password), one=True) # noqa

            self.assertIsNotNone(res)
            self.assertNotEqual(res['auth_data'], '')
            self.assertEqual(res['fail_cnt'],      0)

            with UserLogin(self.fdao, 'FURA') as ul:
                ul.login('bsadmin', tUsrAuth.AuthType_Couplet.key_password, self.TEST_PASSWD)
        finally:
            helper.sql_commit()


    def test_023_usr_reset_token(self):
        if DEBUG: return

        helper.sql_run("delete from fura.usrauth where usr_id = 'bsadmin' and site_id = 1 and auth_type='%s'" % (tUsrAuth.AuthType_Couplet.key_token)) # noqa
        helper.sql_commit()

        try:
            with UserLogin(self.fdao, 'FURA') as ul:
                ul.req_token_reset('bsadmin',
                                   'bsadmin',
                                   tUsrAuth.AuthType_Couplet.key_token)

                res = helper.sql_fetch("select * from fura.usrauth where site_id=1 and usr_id='bsadmin' and auth_type='%s'" % (
                    tUsrAuth.AuthType_Couplet.key_token), one=True) # noqa

                self.assertIsNotNone(res)
                self.assertIsNotNone(res)
                self.assertGreater(len(res['auth_data']),  31)
                # self.assertEqual(res['resettok'], '')
                # self.assertEqual(res['resetexp'], datetime.datetime.min)

                tok = ul.read_token('bsadmin', tUsrAuth.AuthType_Couplet.key_token)

                self.assertIsNotNone(tok)
                self.assertEqual(tok, res['auth_data'])

        finally:
            helper.sql_commit()


    def test_024_usr_login_token(self):
        if DEBUG: return

        try:
            res = helper.sql_fetch("select * from fura.usrauth where site_id=1 and usr_id='bsadmin' and auth_type='%s'" % (tUsrAuth.AuthType_Couplet.key_token), one=True) # noqa
            self.assertIsNotNone(res)
            self.assertGreater(len(res['auth_data']),  31)

            with UserLogin(self.fdao, 'FURA') as ul:
                usr_id = ul.login_token(tUsrAuth.AuthType_Couplet.key_token, res['auth_data'])

                self.assertEqual(usr_id, 'bsadmin')

                usr_id = ul.login_token(tUsrAuth.AuthType_Couplet.key_token, 'foobar', raise_error=False)

                self.assertIsNone(usr_id)

        finally:
            helper.sql_commit()



if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
