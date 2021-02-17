# standard imports
import logging

# local imports
from . import keyapi
from .interface import Keystore
from crypto_dev_signer.error import UnknownAccountError
from crypto_dev_signer.common import strip_hex_prefix

logg = logging.getLogger()


class DictKeystore(Keystore):

    def __init__(self):
        self.keys = {}


    def get(self, address, password=None):
        if password != None:
            logg.debug('password ignored as dictkeystore doesnt do encryption')
        try:
            return self.keys[address]
        except KeyError:
            raise UnknownAccountError(address)


    def import_key(self, pk, password=None):
        pubk = keyapi.private_key_to_public_key(pk)
        address_hex = pubk.to_checksum_address()
        address_hex_clean = strip_hex_prefix(address_hex)
        self.keys[address_hex_clean] = pk.to_bytes()
        return address_hex
