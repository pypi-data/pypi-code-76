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

import asyncio
import logging
import unittest

from databases.core import Connection

from mettle.db.encode_io_databases.aconnect_postgres import AConnectPostgres

from bs_lib.auto_transaction_async import AutoTransactionAsync
from bs_lib.pod_async              import PodAsync

from bs_lib_testing import helper

from bs_fura.access_async      import AccessAsync
from bs_fura.xfura             import xFura
from bs_fura.dao_async         import DaoAsync
from bs_fura.user_login_async  import UserLoginAsync
from bs_fura                   import util

from bs_fura.db.tables.usr_auth import tUsrAuth

from bs_fura.braze import ResetMethod_Couplet


DEBUG   = False
VERBOSE = True
DB_DAO  = 'postgresql'


def setUpModule():
    helper._data['debug']      = DEBUG
    helper._data['verbose']    = VERBOSE
    helper._data['aloop']      = asyncio.get_event_loop()
    helper.init_logger()
    helper.init_environ('fura')


def tearDownModule():
    pass


class TestFuraLibrary(unittest.TestCase):

    TEST_PASSWD = 'h3ll0-World@Q#W'


    @classmethod
    def setUpClass(cls):
        cls.data   = helper._data
        cls.usr_id = '[TestFuraLibrary]'
        cls.aloop  = helper._data['aloop']
        cls.pod = None
        cls.fdao = None
        cls.dbcon = None


    @classmethod
    def tearDownClass(cls):
        pass


    def test_001_initiailize(self):
        self.aloop.run_until_complete(helper.init_database_async())

        self.assertTrue(self.data['database'].is_connected)

        self.data['db_dao'] = util.dao_by_name('postgresql', 'dao_async')

        self.assertIsNotNone(self.data['db_dao'])

        logger = logging.getLogger('databases')

        logger.propagate = False


    async def run_test_all(self):
        async with Connection(self.data['database']._backend) as conn:
            dbcon = AConnectPostgres(conn)
            pod   = PodAsync(None, dbcon, self.data['log'])
            fdao  = DaoAsync(pod, self.data['db_dao'])

            self.dbcon = dbcon
            self.pod   = pod
            self.fdao  = fdao

            print()

            await self.atest_011_access_test_super_user()
            await self.atest_012_access_test_test_user()
            await self.atest_021_usr_login_test()
            await self.atest_022_usr_reset_auth()
            await self.atest_023_usr_reset_token()
            await self.atest_024_usr_login_token()


    def test_003_test_all(self):
        self.aloop.run_until_complete(self.run_test_all())


    async def atest_011_access_test_super_user(self):
        if DEBUG: return

        print('atest_011_access_test_super_user')

        src = __name__

        await helper.sql_arun(self.dbcon, "delete from fura.ada")
        await helper.sql_arun(self.dbcon, "delete from fura.aga")
        await self.dbcon.commit()

        async with AutoTransactionAsync(self.pod) as at:
            async with AccessAsync(self.fdao, 'FURA', 'admin', src) as ac:
                self.assertTrue(ac.ok())
                self.assertTrue(await ac.access('fura.cfg.create'))
                self.assertTrue(await ac.access('fura.site.delete'))
                self.assertTrue(await ac.access('fura.role.update'))

                self.assertTrue(ac.ok())

            await at.commit()

        res = await helper.sql_afetch(self.dbcon, "select * from fura.aga")

        self.assertIsNotNone(res)
        self.assertEqual(3, len(res))


    async def atest_012_access_test_test_user(self):
        if DEBUG: return

        print('atest_012_access_test_test_user')

        src = __name__

        await helper.sql_arun(self.dbcon, "delete from fura.rolefuncrel where site_id = 1 and role_id = 'test'")
        await helper.sql_arun(self.dbcon, "delete from fura.ada")
        await helper.sql_arun(self.dbcon, "delete from fura.aga")
        await self.dbcon.commit()

        async with AutoTransactionAsync(self.pod) as at:
            async with AccessAsync(self.fdao, 'FURA', 'test', src) as ac:
                self.assertTrue(ac.ok())
                self.assertFalse(await ac.access('fura.cfg.create'))
                self.assertFalse(await ac.access('fura.site.delete'))
                self.assertFalse(await ac.access('fura.role.update'))

                self.assertFalse(ac.ok())

            await at.commit()

        res = await helper.sql_afetch(self.dbcon, "select * from fura.ada")

        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))

        await helper.sql_arun(self.dbcon, "delete from fura.ada")
        await helper.sql_arun(self.dbcon, "delete from fura.aga")
        await self.dbcon.commit()

        async with AutoTransactionAsync(self.pod) as at:
            async with AccessAsync(self.fdao, 'FURA', 'test', src) as ac:
                self.assertTrue(ac.ok())
                self.assertFalse(await ac.access('fura.cfg.create',  ignore_ada = True))
                self.assertFalse(await ac.access('fura.site.delete', ignore_ada = True))
                self.assertFalse(await ac.access('fura.role.super',  ignore_ada = True))

                self.assertFalse(ac.ok())

            await at.commit()

        res = await helper.sql_afetch(self.dbcon, "select * from fura.ada")

        self.assertIsNotNone(res)
        self.assertEqual(3, len(res))

        await helper.sql_arun(self.dbcon, "delete from fura.ada")
        await helper.sql_arun(self.dbcon, "delete from fura.aga")
        await helper.sql_arun(self.dbcon, "insert into fura.rolefuncrel values(1, 'test', 'fura.cfg.create', '%s', current_timestamp)" % self.usr_id)  # noqa
        await helper.sql_arun(self.dbcon, "insert into fura.rolefuncrel values(1, 'test', 'fura.cfg.update', '%s', current_timestamp)" % self.usr_id)  # noqa
        await self.dbcon.commit()

        async with AutoTransactionAsync(self.pod) as at:
            async with AccessAsync(self.fdao, 'FURA', 'test', src) as ac:
                self.assertTrue(ac.ok())
                self.assertTrue(await ac.access('fura.cfg.create'))
                self.assertTrue(await ac.access('fura.cfg.update'))
                self.assertFalse(await ac.access('fura.site.delete'))
                self.assertFalse(await ac.access('fura.role.super', ignore_ada = True))

                self.assertFalse(ac.ok())

            await at.commit()

        resd = await helper.sql_afetch(self.dbcon, "select * from fura.ada")
        resg = await helper.sql_afetch(self.dbcon, "select * from fura.aga")

        self.assertIsNotNone(resd)
        self.assertIsNotNone(resg)
        self.assertEqual(2, len(resd))
        self.assertEqual(2, len(resg))

        with self.assertRaises(xFura):
            async with AccessAsync(self.fdao, 'FURA', 'test', src) as ac:
                await ac.required('fura.site.delete')


    async def atest_021_usr_login_test(self):
        if DEBUG: return

        print('atest_021_usr_login_test')

        await helper.sql_arun(self.dbcon, "delete from fura.ula where site_id = 1")
        await helper.sql_arun(self.dbcon, "delete from fura.usrauth where usr_id = 'bsadmin' and site_id = 1")
        await helper.sql_arun(self.dbcon, "delete from fura.usrotp where usr_id = 'bsadmin' and site_id = 1")
        await helper.sql_arun(self.dbcon, "delete from fura.usr where id = 'bsadmin' and site_id = 1")
        await helper.sql_arun(self.dbcon, "insert into fura.usr values(1, 'bsadmin', 'admin', 'A', null, null, null, null, null, null, null, null, null, '%s', current_timestamp, 'sys', false, false, false, false, false, false, false)" % self.usr_id) # noqa
        await self.dbcon.commit()

        from bs_triceraclops.audit_async  import AuditAsync as TriAudit

        tri_audit = TriAudit(self.pod.dbcon, DB_DAO)

        try:
            async with UserLoginAsync(self.fdao, 'FURA') as ul:
                await ul.set_auth_data(tri_audit,
                                       'bsadmin',
                                       tUsrAuth.AuthType_Couplet.key_password,
                                       self.TEST_PASSWD,
                                       None,
                                       None)

            async with UserLoginAsync(self.fdao, 'FURA') as ul:
                await ul.login('bsadmin', tUsrAuth.AuthType_Couplet.key_password, self.TEST_PASSWD)

        finally:
            await self.dbcon.commit()

        res = await helper.sql_afetch(self.dbcon, "select * from fura.ula where site_id = 1 and usr_id = 'bsadmin'")

        self.assertEqual(2,  len(res))
        self.assertEqual('S', res[0]['state'])
        self.assertEqual('S', res[1]['state'])


    async def atest_022_usr_reset_auth(self):
        if DEBUG: return

        print('atest_022_usr_reset_auth')

        await helper.sql_arun(self.dbcon, "delete from fura.usrauth where usr_id = 'bsadmin' and site_id = 1")
        await self.dbcon.commit()

        from bs_triceraclops.audit_async  import AuditAsync as TriAudit

        tri_audit = TriAudit(self.pod.dbcon, DB_DAO)

        try:
            async with UserLoginAsync(self.fdao, 'FURA') as ul:
                tok = await ul.reset_auth('bsadmin',
                                          tUsrAuth.AuthType_Couplet.key_password,
                                          ResetMethod_Couplet.key_email,
                                          None)

                await self.dbcon.commit()

            self.assertIsNotNone(tok)

            res = await helper.sql_afetch(
                self.dbcon,
                "select * from fura.usrotp where site_id=1 and usr_id='bsadmin' and target='auth-reset'",
                one=True)

            self.assertIsNotNone(res)
            self.assertEqual(res['otp'],        tok)
            self.assertNotEqual(res['expire'],  None)
            self.assertEqual(res['used'],       False)
            self.assertEqual(res['fail_cnt'],   0)

            async with UserLoginAsync(self.fdao, 'FURA') as ul:
                await ul.set_auth_data(tri_audit,
                                       'bsadmin',
                                       tUsrAuth.AuthType_Couplet.key_password,
                                       self.TEST_PASSWD,
                                       tok,
                                       ResetMethod_Couplet.key_email)

            res = await helper.sql_afetch(
                self.dbcon,
                "select * from fura.usrauth where site_id=1 and usr_id='bsadmin' and auth_type='%s'" % (
                    tUsrAuth.AuthType_Couplet.key_password),
                one=True)

            self.assertIsNotNone(res)
            self.assertNotEqual(res['auth_data'], '')
            self.assertEqual(res['fail_cnt'],      0)

            async with UserLoginAsync(self.fdao, 'FURA') as ul:
                await ul.login('bsadmin', tUsrAuth.AuthType_Couplet.key_password, self.TEST_PASSWD)

        finally:
            await self.dbcon.commit()


    async def atest_023_usr_reset_token(self):
        if DEBUG: return

        print('atest_023_usr_reset_token')

        await helper.sql_arun(
            self.dbcon,
            "delete from fura.usrauth where usr_id = 'bsadmin' and site_id = 1 and auth_type='%s'" % (
                tUsrAuth.AuthType_Couplet.key_token)
        )

        await self.dbcon.commit()

        try:
            async with UserLoginAsync(self.fdao, 'FURA') as ul:
                await ul.req_token_reset('bsadmin',
                                         'bsadmin',
                                         tUsrAuth.AuthType_Couplet.key_token)

                res = await helper.sql_afetch(
                    self.dbcon,
                    "select * from fura.usrauth where site_id=1 and usr_id='bsadmin' and auth_type='%s'" % (
                        tUsrAuth.AuthType_Couplet.key_token),
                    one=True)

                self.assertIsNotNone(res)
                self.assertIsNotNone(res)
                self.assertGreater(len(res['auth_data']),  31)

                tok = await ul.read_token('bsadmin', tUsrAuth.AuthType_Couplet.key_token)

                self.assertIsNotNone(tok)
                self.assertEqual(tok, res['auth_data'])

        finally:
            await self.dbcon.commit()


    async def atest_024_usr_login_token(self):
        if DEBUG: return

        print('atest_024_usr_login_token')

        try:
            res = await helper.sql_afetch(
                self.dbcon,
                "select * from fura.usrauth where site_id=1 and usr_id='bsadmin' and auth_type='%s'" % (
                    tUsrAuth.AuthType_Couplet.key_token),
                one=True)

            self.assertIsNotNone(res)
            self.assertGreater(len(res['auth_data']),  31)

            async with UserLoginAsync(self.fdao, 'FURA') as ul:
                usr_id = await ul.login_token(tUsrAuth.AuthType_Couplet.key_token, res['auth_data'])

                self.assertEqual(usr_id, 'bsadmin')

                usr_id = await ul.login_token(tUsrAuth.AuthType_Couplet.key_token, 'foobar', raise_error=False)

                self.assertIsNone(usr_id)

        finally:
            await self.dbcon.commit()



if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
