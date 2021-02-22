"""
Various cryptographic utilities.
"""
import os
from base64 import b64encode

# minimum viable key size to produce a strong encryption key
MIN_KEY_SIZE = 8


def generate_strong_encryption_key(key_size=64):
    """
    Generated cryptographically strong encryption key.
    :param key_size: the optional size of the key (defaults to 64). Must be greater than or equal to MIN_KEY_SIZE.
    :return: a cryptographically strong string.
    """
    if key_size < MIN_KEY_SIZE:
        raise ValueError(f'Key size must be a positive integer greater than {MIN_KEY_SIZE}')
    return b64encode(os.urandom(key_size)).decode('utf-8')
