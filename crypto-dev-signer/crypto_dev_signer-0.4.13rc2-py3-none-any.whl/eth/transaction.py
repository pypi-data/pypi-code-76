# standard imports
import logging
import binascii

# third-party imports
from rlp import encode as rlp_encode

# local imports
from crypto_dev_signer.common import strip_hex_prefix, add_hex_prefix

logg = logging.getLogger(__name__)


class Transaction:
    
    def rlp_serialize(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError


class EIP155Transaction:

    def __init__(self, tx, nonce, chainId=1):
       
        to = binascii.unhexlify(strip_hex_prefix(tx['to']))
        data = binascii.unhexlify(strip_hex_prefix(tx['data']))

        gas_price = None
        start_gas = None
        value = None

        try:
            gas_price = int(tx['gasPrice'])
        except ValueError:
            gas_price = int(tx['gasPrice'], 16)
        byts = ((gas_price.bit_length()-1)/8)+1
        gas_price = gas_price.to_bytes(int(byts), 'big')

        try:
            start_gas = int(tx['gas'])
        except ValueError:
            start_gas = int(tx['gas'], 16)
        byts = ((start_gas.bit_length()-1)/8)+1
        start_gas = start_gas.to_bytes(int(byts), 'big')

        try:
            value = int(tx['value'])
        except ValueError:
            value = int(tx['value'], 16)
        byts = ((value.bit_length()-1)/8)+1
        value = value.to_bytes(int(byts), 'big')

        try:
            nonce = int(nonce)
        except ValueError:
            nonce = int(nonce, 16)
        byts = ((nonce.bit_length()-1)/8)+1
        nonce = nonce.to_bytes(int(byts), 'big')

        try:
            chainId = int(chainId)
        except ValueError:
            chainId = int(chainId, 16)
        byts = ((chainId.bit_length()-1)/8)+1
        chainId = chainId.to_bytes(int(byts), 'big')

        self.nonce = nonce
        self.gas_price = gas_price
        self.start_gas = start_gas
        self.to = to
        self.value = value
        self.data = data
        self.v = chainId
        self.r = b''
        self.s = b''
        self.sender = strip_hex_prefix(tx['from'])


    def rlp_serialize(self):
        s = [
            self.nonce,
            self.gas_price,
            self.start_gas,
            self.to,
            self.value,
            self.data,
            self.v,
            self.r,
            self.s,
                ]
        return rlp_encode(s)

    def serialize(self):
        tx = {
            'nonce': add_hex_prefix(self.nonce.hex()),
            'gasPrice': add_hex_prefix(self.gas_price.hex()),
            'gas': add_hex_prefix(self.start_gas.hex()),
            'to': add_hex_prefix(self.to.hex()),
            'value': add_hex_prefix(self.value.hex()),
            'data': add_hex_prefix(self.data.hex()),
            'v': add_hex_prefix(self.v.hex()),
            'r': add_hex_prefix(self.r.hex()),
            's': add_hex_prefix(self.s.hex()),
            }
        if tx['data'] == '':
            tx['data'] = '0x'

        if tx['value'] == '':
            tx['value'] = '0x00'

        if tx['nonce'] == '':
            tx['nonce'] = '0x00'

        return tx
