'''
This module provides interfaces for ECDH and ECDSA.
The only interface exposed is ECKeys.

Usage:
>>> k1 = ECKeys()
>>> k2 = ECKeys()
>>> k1.load(k2.export()) # load / export as bytes
>>> k2.loadHex(k1.exportHex()) # load / export as hex string.
>>> k1.secret() == k2.secret() # shared secrets
True
>>> k2.verify(b'data', k1.sign(b'data')) # digital signatures
True
'''

from ecdsa import SigningKey, VerifyingKey, ECDH, NIST256p, BadSignatureError
from curva import CurvaError
from hashlib import sha384
from typing import Tuple

EPHEMERAL_KEY_LENGTH = NIST256p.verifying_key_length

class KeyProtocolError(CurvaError):
    'General base class for key protocol errors.'

class MissingRemoteKey(KeyProtocolError):
    'No remote key was specified.'
    def __init__(self):
        super().__init__('no remote key was given.')

class ECKeys:
    'Represents a pair of elliptic-curve keys.'
    def __init__(self):
        self._privateKey = SigningKey.generate(NIST256p, hashfunc=sha384)
        self._publicKey = self._privateKey.get_verifying_key()
        self._remoteKey = None
    def _check_key(self) -> None:
        if self._remoteKey is None:
            raise MissingRemoteKey
    def load(self, key: bytes) -> None:
        'Loads a remote public key as bytes.'
        self._remoteKey = VerifyingKey.from_string(key, NIST256p, hashfunc=sha384)
    def loadHex(self, key: str) -> None:
        'Loads a remote public key as hex string.'
        self.load(bytes.fromhex(key))
    def export(self) -> bytes:
        'Exports the local public key as bytes.'
        return self._publicKey.to_string()
    def exportHex(self) -> bytes:
        'Exports the local public key as hex string.'
        return self.export().hex()
    def secret(self) -> bytes:
        'Gets the shared secret.'
        self._check_key()
        return ECDH(NIST256p, self._privateKey, self._remoteKey).generate_sharedsecret_bytes()
    def _ephemeral(self, data: bytes=None) -> Tuple[bytes, bytes]:
        'Generates or extracts ephemeral keys.'
        if data is None:
            self._check_key()
            key = SigningKey.generate(NIST256p, hashfunc=sha384)
            secret = ECDH(NIST256p, key, self._remoteKey).generate_sharedsecret_bytes()
            return key.get_verifying_key().to_string(), secret
        else:
            key, data = data[:EPHEMERAL_KEY_LENGTH], data[EPHEMERAL_KEY_LENGTH:]
            key = VerifyingKey.from_string(key, NIST256p, hashfunc=sha384)
            secret = ECDH(NIST256p, self._privateKey, key).generate_sharedsecret_bytes()
            return secret, data
    def sign(self, data: bytes) -> bytes:
        'Signs the data with local private key.'
        return self._privateKey.sign(data, hashfunc=sha384)
    def verify(self, data: bytes, signature: bytes) -> bool:
        'Verified the data with remote public key.'
        self._check_key()
        try:
            self._remoteKey.verify(signature, data, hashfunc=sha384)
            return True
        except BadSignatureError:
            return False