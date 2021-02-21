import binascii
import os
import random
import secrets
import string


def token(nBytes=16, urlsafe=False, raw=False):
    if raw:
        return secrets.token_bytes(nBytes)
    if urlsafe:
        return secrets.token_urlsafe(nBytes)
    return secrets.token_hex(nBytes)


def tokenRandom(nBytes=16, asString=True):
    return binascii.hexlify(os.urandom(nBytes)).decode("UTF-8")


def randomLetters(length=8, punctuation=False):
    char_set = string.ascii_letters
    if punctuation:
        char_set += string.punctuation
    urand = random.SystemRandom()
    return "".join([urand.choice(char_set) for _ in range(length)])
