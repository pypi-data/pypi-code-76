r'''
This module provides interfaces exposed as functions to AES encryptions and HKDF key deriviations.

Usage:
>>> d = encrypt(b'key', b'data') # encryption
>>> decrypt(b'key', d) # decryption
b'data'
>>> d = pad_data(b'data') # padding
>>> d
b'data\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c'
>>> unpad_data(d) # unpadding
b'data'
'''

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA512
from typing import Tuple
from curva import CurvaError
import os

__all__ = ['encrypt', 'decrypt', 'pad_data', 'unpad_data', 'CryptographyError', 'InvalidPadding']

AES_KEY_SIZE = 32
AES_BLOCK_SIZE = AES.block_size

LENGTH_SALT = SHA512.digest_size
LENGTH_IV = AES.block_size

class CryptographyError(CurvaError):
    'General base class for cryptographic errors.'

class InvalidPadding(CryptographyError):
    'PKCS-5 Padding is invalid.'
    def __init__(self, padding: bytes):
        super().__init__(padding)

def random_salt_iv() -> Tuple[bytes, bytes]:
    'Generates a pair of random salt and initial vector.'
    return os.urandom(LENGTH_SALT), os.urandom(LENGTH_IV)

def extract_salt_iv(data: bytes) -> Tuple[bytes, bytes, bytes]:
    'Extracts a pair of salt and initial vector from data.'
    return data[:LENGTH_SALT], data[LENGTH_SALT:LENGTH_SALT+LENGTH_IV], data[LENGTH_SALT+LENGTH_IV:]

def derive_key(key: bytes, salt: bytes) -> bytes:
    'Derives a symmetric key from given master and salt.'
    return HKDF(key, AES_KEY_SIZE, salt, SHA512)

def pad_data(data: bytes, size: int=AES_BLOCK_SIZE) -> bytes:
    'Pads data using PKCS-5 standard.'
    needs = size - len(data) % size
    padding = bytes((needs, ) * needs)
    return data+padding

def unpad_data(data: bytes) -> bytes:
    'Unpads data using PKCS-5 standard.'
    needs = data[-1]
    padding, data = data[-needs:], data[:-needs]
    if padding != bytes((needs, ) * needs):
        raise InvalidPadding(padding)
    return data

def encrypt(key: bytes, data: bytes) -> bytes:
    'Encrypts binary data using given key.'
    salt, iv = random_salt_iv()
    key = derive_key(key, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = pad_data(data)
    return salt+iv+cipher.encrypt(data)

def decrypt(key: bytes, data: bytes) -> bytes:
    'Decrypts binary data using given key.'
    salt, iv, data = extract_salt_iv(data)
    key = derive_key(key, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.decrypt(data)
    return unpad_data(data)
