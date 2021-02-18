from rsa import PrivateKey, decrypt
import os


def decrypt(key_path: str, val: str):
    if not os.path.exists(key_path) or not os.path.isfile(key_path):
        raise Exception(f'Key does not exist at {key_path}')

    with open(key_path, 'r') as fd:
        pkey = PrivateKey.load_pkcs1(fd.read().encode())

    return decrypt(bytes(val), pkey).decode('utf-8')


v = decrypt('../rsa_keys/rsa_1024.dev.pem', 'W2u5r/ff3KkoOEldPzml1mAlnfakS3w6TUqrii5s7iIedzJf/uOT18rH28E46sZMDJFJjKw9TtQVlCG+60TU7lEFq9o8qmcTfjqCKQ/UaFWa656SPTl6hHCH03Kf02/ZaAW1KNIWA40NGosor0gw2/pVHKB0l76BLc2l6CVSmuc=')
print(v)
