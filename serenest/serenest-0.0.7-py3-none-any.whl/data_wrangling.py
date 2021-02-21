#!/usr/bin/env python3

import binascii

def hexstring_to_binary(hexstring: str) -> str:
    return binascii.unhexlify(hexstring)

def binary_to_hexstring(binary):
    return binascii.hexlify(binary)

def bytes_to_bytearray(my_bytes):
    return list(my_bytes)

def bytearray_to_bytes(list_of_bytes):
    return bytes(list_of_bytes)




