import logging
import sha3

from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend

keys = KeyAPI(NativeECCBackend)
logg = logging.getLogger(__name__)


class Signer:


    def __init__(self, keyGetter):
        self.keyGetter = keyGetter


    def signTransaction(self, tx, password=None):
        raise NotImplementedError



class ReferenceSigner(Signer):
   

    def __init__(self, keyGetter):
        super(ReferenceSigner, self).__init__(keyGetter)


    def signTransaction(self, tx, password=None):
        s = tx.rlp_serialize()
        h = sha3.keccak_256()
        h.update(s)
        g = h.digest()
        k = keys.PrivateKey(self.keyGetter.get(tx.sender, password))
        z = keys.ecdsa_sign(message_hash=g, private_key=k)
        vnum = int.from_bytes(tx.v, 'big')
        v = (vnum * 2) + 35 + z[64]
        byts = ((v.bit_length()-1)/8)+1
        tx.v = v.to_bytes(int(byts), 'big')
        tx.r = z[:32]
        tx.s = z[32:64]
        if tx.r[0] == 0:
            tx.r = tx.r[1:]
        if tx.s[0] == 0:
            tx.s = tx.s[1:]
        return z


    def signEthereumMessage(self, address, message, password=None):
        #msg = b'\x19Ethereum Signed Message:\n{}{}'.format(len(message), message)
        k = keys.PrivateKey(self.keyGetter.get(address, password))
        #z = keys.ecdsa_sign(message_hash=g, private_key=k)
        z = None
        if type(message).__name__ == 'str':
            logg.debug('signing message in "str" format: {}'.format(message))
            z = k.sign_msg(bytes.fromhex(message))
        elif type(message).__name__ == 'bytes':
            logg.debug('signing message in "bytes" format: {}'.format(message.hex()))
            z = k.sign_msg(message)
        else:
            raise ValueError('message must be type str or bytes, received {}'.format(type(message).__name__))
        return z

