import argparse
from random import randint

BOMER_CRYPTO_MASKS_COUNT = 30
BOMER_CRYPTO_MAGIC = 0xA5
BOMER_CRYPTO_MASKS = [
    0x4F, 0xAA, 0xC4, 0xF3, 0x45,
    0x23, 0xCD, 0xBE, 0xEF, 0xCC,
    0xF2, 0xBB, 0xDE, 0xAD, 0x9E,
    0xC3, 0xAA, 0xC4, 0xF3, 0x5D,
    0x12, 0x3B, 0xAE, 0xBE, 0xEF,
    0x23, 0xCD, 0xBE, 0xEF, 0xCC
]


def encode(data):
    data = bytearray(data, encoding="utf-8")
    checksum = 0
    encoded = []
    data_len = len(data)
    mask_index = randint(0, BOMER_CRYPTO_MASKS_COUNT - 1)
    encoded.append((mask_index ^ BOMER_CRYPTO_MAGIC))
    for b in data:
        b = int(b)
        mask = BOMER_CRYPTO_MASKS[mask_index]
        encoded_byte = (b & 0xFF) ^ mask
        encoded.append(encoded_byte & 0xFF)
        checksum += encoded_byte
        mask_index = (mask_index + 1) % BOMER_CRYPTO_MASKS_COUNT
    encoded.append(((checksum & 0xFF) ^ (0xFF - BOMER_CRYPTO_MAGIC)) & 0xFF)
    return bytearray(encoded)


def decode(data):
    data = bytearray(data)
    checksum = 0
    encoded = []
    data_len = len(data)
    mask_index = (data[0] ^ BOMER_CRYPTO_MAGIC) & 0xFF
    for b in data[1:data_len - 1]:
        mask = BOMER_CRYPTO_MASKS[mask_index]
        checksum += b & 0xFF
        encoded_byte = (b ^ mask) & 0xFF
        encoded.append(encoded_byte)
        mask_index = (mask_index + 1) % BOMER_CRYPTO_MASKS_COUNT
    checksum = (checksum & 0xFF) ^ (0xFF - BOMER_CRYPTO_MAGIC)
    data_checksum = data[-1]
    if checksum != data_checksum:
        print("!!")
    return bytearray(encoded).decode("utf-8")
