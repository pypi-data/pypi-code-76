# standard imports
import logging
import time

# third-party imports
from crypto_dev_signer.eth.transaction import EIP155Transaction

# local imports
from crypto_dev_signer.error import TransactionRevertError

logg = logging.getLogger()


class TxExecutor:

    def __init__(self, sender, signer, translator, dispatcher, reporter, nonce, chain_id, fee_helper=None, fee_price_helper=None, verifier=None, block=False):
        self.sender = sender
        self.translator = translator
        self.nonce = nonce
        self.signer = signer
        self.dispatcher = dispatcher
        self.reporter = reporter
        self.block = bool(block)
        self.chain_id = chain_id
        self.tx_hashes = []
        if fee_helper == None:
            fee_helper = self.noop_fee_helper
        self.fee_helper = fee_helper
        if fee_price_helper == None:
            fee_price_helper = self.noop_fee_price_helper
        self.fee_price_helper = fee_price_helper
        if verifier == None:
            verifier = self.noop_verifier
        self.verifier = verifier


    def noop_fee_helper(self, tx):
        return 1


    def noop_fee_price_helper(self):
        return 1


    def noop_verifier(self, rcpt):
        return rcpt


    def noop_translator(self, tx):
        return tx


    def sign_and_send(self, builder, force_wait=False):

        fee_price = self.fee_price_helper()

        tx_tpl = {
            'from': self.sender,
            'chainId': self.chain_id,
            'feeUnits': 0, #fee_units,
            'feePrice': fee_price,
            'nonce': self.nonce,
            }

        tx = self.translator(tx_tpl)
        for b in builder:
            tx = b(tx)

        tx['feeUnits'] = self.fee_helper(tx)
        tx = self.translator(tx)

        logg.debug('from {} nonce {} tx {}'.format(self.sender, self.nonce, tx))

        chain_tx = EIP155Transaction(tx, self.nonce, self.chain_id)
        signature = self.signer.signTransaction(chain_tx)
        chain_tx_serialized = chain_tx.rlp_serialize()
        tx_hash = self.dispatcher('0x' + chain_tx_serialized.hex())
        self.tx_hashes.append(tx_hash)
        self.nonce += 1
        rcpt = None
        if self.block or force_wait:
            rcpt = self.wait_for(tx_hash)
        return (tx_hash.hex(), rcpt)


    def wait_for(self, tx_hash=None):
        if tx_hash == None:
            tx_hash = self.tx_hashes[len(self.tx_hashes)-1]
        i = 1
        while True:
            try:
                #return self.w3.eth.getTransactionReceipt(tx_hash)
                return self.reporter(tx_hash)
            except Exception:
                logg.debug('poll #{} for {}'.format(i, tx_hash.hex()))   
                i += 1
                time.sleep(1)
        return self.verifier(rcpt)
