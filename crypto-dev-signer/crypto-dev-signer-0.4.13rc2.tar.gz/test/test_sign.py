#!/usr/bin/python

import unittest
import logging

from rlp import encode as rlp_encode

from crypto_dev_signer.eth.signer import ReferenceSigner
from crypto_dev_signer.eth.transaction import EIP155Transaction

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


tx_ints = {
    'nonce': 0,
    'from': "0xEB014f8c8B418Db6b45774c326A0E64C78914dC0",
    'gasPrice': "20000000000",
    'gas': "21000",
    'to': '0x3535353535353535353535353535353535353535',
    'value': "1000",
    'data': "deadbeef",
}

tx_hexs = {
    'nonce': '0x0',
    'from': "0xEB014f8c8B418Db6b45774c326A0E64C78914dC0",
    'gasPrice': "0x4a817c800",
    'gas': "0x5208",
    'to': '0x3535353535353535353535353535353535353535',
    'value': "0x3e8",
    'data': "deadbeef",
}

class pkGetter:

    def __init__(self, pk):
        self.pk = pk

    def get(self, address, password=None):
        return self.pk


class TestSign(unittest.TestCase):

    pk = None
    nonce = -1
    pk_getter = None


    def getNonce(self):
        self.nonce += 1
        return self.nonce


    def setUp(self):
        self.pk = bytes.fromhex('5087503f0a9cc35b38665955eb830c63f778453dd11b8fa5bd04bc41fd2cc6d6')
        self.pk_getter = pkGetter(self.pk)


    def tearDown(self):
        logg.info('teardown empty')



    # TODO: verify rlp tx output
    def test_serialize_transaction(self):
        t = EIP155Transaction(tx_ints, 0)
        self.assertRegex(t.__class__.__name__, "Transaction")
        s = t.serialize()
        self.assertEqual('{}'.format(s), "{'nonce': '', 'gasPrice': '0x04a817c800', 'gas': '0x5208', 'to': '0x3535353535353535353535353535353535353535', 'value': '0x03e8', 'data': '0xdeadbeef', 'v': '0x01', 'r': '', 's': ''}")
        r = t.rlp_serialize()
        self.assertEqual(r.hex(), 'ea808504a817c8008252089435353535353535353535353535353535353535358203e884deadbeef018080')

        t = EIP155Transaction(tx_hexs, 0)
        self.assertRegex(t.__class__.__name__, "Transaction")
        s = t.serialize()
        self.assertEqual('{}'.format(s), "{'nonce': '', 'gasPrice': '0x04a817c800', 'gas': '0x5208', 'to': '0x3535353535353535353535353535353535353535', 'value': '0x03e8', 'data': '0xdeadbeef', 'v': '0x01', 'r': '', 's': ''}")
        r = t.rlp_serialize()
        self.assertEqual(r.hex(), 'ea808504a817c8008252089435353535353535353535353535353535353535358203e884deadbeef018080')



    def test_sign_transaction(self):
        t = EIP155Transaction(tx_ints, 461, 8995)
        s = ReferenceSigner(self.pk_getter)
        z = s.signTransaction(t)


    def test_sign_message(self):
        s = ReferenceSigner(self.pk_getter)
        z = s.signEthereumMessage(tx_ints['from'], '666f6f')
        z = s.signEthereumMessage(tx_ints['from'], b'foo')
        logg.debug('zzz {}'.format(str(z)))


if __name__ == '__main__':
    unittest.main()
