# standard imports
import unittest
import logging
import os

# third-party imports
import web3

# local imports
from crypto_dev_signer.keystore import DictKeystore
from crypto_dev_signer.eth.signer import ReferenceSigner
from crypto_dev_signer.helper import TxExecutor
from crypto_dev_signer.eth.helper import EthTxExecutor

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

script_dir = os.path.realpath(os.path.dirname(__file__))


class MockEthTxBackend:

    def dispatcher(self, tx):
        logg.debug('sender {}'.format(tx))
        return os.urandom(32)

    def reporter(self, tx):
        logg.debug('reporter {}'.format(tx))

    def verifier(self, rcpt):
        logg.debug('reporter {}'.format(rcpt))

    def fee_price_helper(self):
        return 21

    def fee_helper(self, tx):
        logg.debug('fee helper tx {}'.format(tx))
        return 2

    def builder(self, tx):
        return tx
        
    def builder_two(self, tx):
        tx['value'] = 10243
        tx['to'] = web3.Web3.toChecksumAddress('0x' + os.urandom(20).hex())
        tx['data'] = ''
        if tx.get('feePrice') != None:
            tx['gasPrice'] = tx['feePrice']
            del tx['feePrice']
        if tx.get('feeUnits') != None:
            tx['gas'] = tx['feeUnits']
            del tx['feeUnits']
        return tx


class TestHelper(unittest.TestCase):

    def setUp(self):
        logg.debug('setup')
        self.db = DictKeystore()
        
        keystore_filename = 'UTC--2021-01-08T18-37-01.187235289Z--00a329c0648769a73afac7f9381e08fb43dbea72'
        keystore_filepath = os.path.join(script_dir, 'testdata', keystore_filename)

        self.address_hex = self.db.import_keystore_file(keystore_filepath, '')
        self.signer = ReferenceSigner(self.db)


    def tearDown(self):
        pass


    def test_helper(self):
        backend = MockEthTxBackend()
        executor = TxExecutor(self.address_hex, self.signer, backend.builder, backend.dispatcher, backend.reporter, 666, 13, backend.fee_helper, backend.fee_price_helper, backend.verifier)    

        tx_ish = {'from': self.address_hex}
        executor.sign_and_send([backend.builder_two])


    def test_eth_helper(self):
        backend = MockEthTxBackend()
        w3 = web3.Web3(web3.Web3.HTTPProvider('http://localhost:8545'))
        executor = EthTxExecutor(w3, self.address_hex, self.signer, 1337)

        tx_ish = {'from': self.address_hex}
        #executor.sign_and_send([backend.builder, backend.builder_two])
        with self.assertRaises(ValueError): 
            executor.sign_and_send([backend.builder_two])


if __name__ == '__main__':
    unittest.main()
