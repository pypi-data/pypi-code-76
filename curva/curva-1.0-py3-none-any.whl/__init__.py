'''
Curva - A module for Elliptic-Curve Integrated Encryption Scheme (ECIES) based on AES and HKDF.
This module also provides interfaces for Elliptic-Curve Diffie-Hellman (ECDH) and Elliptic-Curve Digital Signature Algorithm (ECDSA).

The only interface exposed to the user is Curva, which integrates all functions mentioned above.

Usage:
>>> c1 = Curva()
>>> c2 = Curva()
>>> c1.load(c2.export()) # load / export as bytes
>>> c2.loadHex(c1.exportHex()) # load / export as hex string
>>> c1.secret() == c2.secret() # calculate shared secret
True
>>> signature = c1.sign(b'data') # digital signature
>>> c2.verify(b'data', signature) # verify
True
>>> c2.decrypt(c1.encrypt(b'data')) # encrypt / decrypt
b'data'
'''

__all__ = ['Curva', 'CurvaError']

class CurvaError(Exception):
    'General base class for curva errors.'

from .key import ECKeys
from .aes import *

class Curva(ECKeys):
    'Public interfaces of curva.'
    def encrypt(self, data: bytes) -> bytes:
        key, secret = self._ephemeral()
        data = encrypt(secret, data)
        return key+data
    def decrypt(self, data: bytes) -> bytes:
        secret, data = self._ephemeral(data)
        data = decrypt(secret, data)
        return data
