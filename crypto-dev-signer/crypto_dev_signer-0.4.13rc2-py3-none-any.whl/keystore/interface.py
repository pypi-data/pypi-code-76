# standard imports
import os

# third-party imports
import eth_keyfile 

# local imports
from . import keyapi


class Keystore:

    def get(self, address, password=None):
        raise NotImplementedError


    def new(self, password=None):
        b = os.urandom(32)
        return self.import_raw_key(b, password)


    def import_raw_key(self, b, password=None):
        pk = keyapi.PrivateKey(b)
        return self.import_key(pk, password)


    def import_key(self, pk, password=None):
        raise NotImplementedError


    def import_keystore_data(self, keystore_content, password=''):
        #private_key = w3.eth.account.decrypt(keystore_content, password)
        private_key = eth_keyfile.decode_keyfile_json(keystore_content, password.encode('utf-8'))
        return self.import_raw_key(private_key, password)

    def import_keystore_file(self, keystore_file, password=''):
        keystore_content = eth_keyfile.load_keyfile(keystore_file)
        return self.import_keystore_data(keystore_content, password)
