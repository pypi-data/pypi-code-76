from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import base64


def encrypt(key_path: str, val: str):
    if not os.path.exists(key_path) or not os.path.isfile(key_path):
        raise Exception(f'Key does not exist at {key_path}')
    key = RSA.import_key(open(key_path, 'r').read())
    return base64.b64encode(PKCS1_OAEP.new(key).encrypt(val.encode('utf-8'))).decode('utf-8')


def decrypt(key_path: str, val: str):
    if not os.path.exists(key_path) or not os.path.isfile(key_path):
        raise Exception(f'Key does not exist at {key_path}')

    pkey = RSA.import_key(open(key_path, 'r').read())
    return PKCS1_OAEP.new(pkey).decrypt(base64.b64decode(val.encode('utf-8'))).decode('utf-8')
