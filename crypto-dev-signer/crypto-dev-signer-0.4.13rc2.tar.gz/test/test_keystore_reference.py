#!/usr/bin/python

# standard imports
import unittest
import logging
import base64
import os

# third-party imports
import psycopg2
from psycopg2 import sql
from cryptography.fernet import Fernet, InvalidToken

# local imports
from crypto_dev_signer.keystore import ReferenceKeystore
from crypto_dev_signer.error import UnknownAccountError

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestDatabase(unittest.TestCase):

    conn = None
    cur = None
    symkey = None
    address_hex = None
    db = None

    def setUp(self):
        logg.debug('setup')
        # arbitrary value
        symkey_hex = 'E92431CAEE69313A7BE9E443C4ABEED9BF8157E9A13553B4D5D6E7D51B5021D9'
        self.symkey = bytes.fromhex(symkey_hex)
        self.address_hex = '9FA61f0E52A5C51b43f0d32404625BC436bb7041'

        kw = {
                'symmetric_key': self.symkey,
                }
        self.db = ReferenceKeystore('postgres+psycopg2://postgres@localhost:5432/signer_test', **kw)
        self.address_hex = self.db.new('foo')


    def tearDown(self):
        self.db.db_session.execute('DROP INDEX ethereum_address_idx;')
        self.db.db_session.execute('DROP TABLE ethereum;')
        self.db.db_session.commit()



    def test_get_key(self):
        logg.debug('getting {}'.format(self.address_hex))
        self.db.get(self.address_hex, 'foo')
        with self.assertRaises(InvalidToken):
           self.db.get(self.address_hex, 'bar')

        bogus_account = '0x' + os.urandom(20).hex()
        with self.assertRaises(UnknownAccountError):
           self.db.get(bogus_account, 'bar')


if __name__ == '__main__':
    unittest.main()
