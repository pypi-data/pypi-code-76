#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import hmac
import binascii
import base64
import os
if os.name == "nt":
    import _locale
    _locale._gdl_bak = _locale._getdefaultlocale
    _locale._getdefaultlocale = (lambda *args: (_locale._gdl_bak()[0], 'utf8'))
from typing import Union
from Crypto.Cipher import AES


def crc32(text: str) -> str:
    return str(binascii.crc32(text.encode()))


def sha512(text: str) -> str:
    return hashlib.sha512(text.encode()).hexdigest().upper()


def sha3_512(text: Union[bytes, str]) -> str:
    #hashout = hmac.new(b'', b'', 'sha3_512')
    hashout = hashlib.sha3_512()
    if isinstance(text, bytes):
        hashout.update(text)
    else:
        hashout.update(text.encode())
    return hashout.hexdigest().upper()


def aes128_decrypt(text: str, key: str) -> str:
    # A workaround because NAV uses PHP version of unsafe openssl based AES-128-ECB which is not directly compatible with raw AES
    def unpad(s): return s[0:-ord(s[-1])]
    decobj = AES.new(key.encode()[:16], AES.MODE_ECB)
    data = decobj.decrypt(base64.decodebytes(text.encode("utf8")))
    return unpad(data.decode("utf8"))
