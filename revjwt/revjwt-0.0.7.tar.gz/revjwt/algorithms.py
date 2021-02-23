import boto3
from jwt.algorithms import Algorithm, RSAAlgorithm
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
    load_ssh_public_key,
)



class KMSAlgorithm(RSAAlgorithm):
    region = 'ap-northeast-1'

    def __init__(self, *args, **kwargs):
        self.hash_alg = RSAAlgorithm.SHA256

    def get_client(self):
        client = boto3.client('kms', self.region)
        return client

    def prepare_key(self, key):
        return key

    def sign(self, msg, key):
        client = self.get_client()
        resp = client.sign(KeyId=key, Message=msg, SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256')
        return resp['Signature']

    def verify(self, msg, key, sig):
        real_key = load_pem_public_key(key)
        return super().verify(msg, real_key, sig)
