from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from binascii import hexlify


class RSAEncryption:

    def __init__(self, private_key=None):
        if private_key is None:
            setattr(self, '__private_key__', RSA.generate(2048))
        else:
            setattr(self, '__private_key__', private_key)

    @property
    def private_key(self):
        """
        :return: return private key with 2048 bits
        """
        return getattr(self, '__private_key__').export_key().decode()

    def public_key(self):
        return getattr(self, '__private_key__').publickey().export_key().decode()

    def _import_key(self, public_key):
        return RSA.import_key(public_key)

    def encrypt(self, message, public_key):
        public_key = self._import_key(public_key)
        cipher = PKCS1_OAEP.new(
            key=public_key,
            hashAlgo=SHA256
        )
        encrypted_message = cipher.encrypt(message=message)

        return encrypted_message

    def decrypt(self, encrypted_message):
        private_key = getattr(self, '__private_key__')
        decrypt = PKCS1_OAEP.new(key=private_key)
        decrypted_message = decrypt.decrypt(encrypted_message)
        return decrypted_message
