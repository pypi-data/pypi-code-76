from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import os
from Crypto import Random
from Crypto.Hash import SHA1
from Crypto.Signature import pkcs1_15


class CRSAHelper:
    def __init__(self, *args):
        if args:
            self.basePath = os.path.join(os.getcwd(), *args)
        else:
            self.basePath = os.getcwd()
        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

    def create_key(self):
        # 伪随机数生成器
        random_generator = Random.new().read
        # rsa算法生成实例
        rsa = RSA.generate(1024, random_generator)

        # 秘钥对的生成
        private_pem = rsa.exportKey()
        if not os.path.exists(os.path.join(self.basePath, 'private.pem')):
            with open(os.path.join(self.basePath, 'private.pem'), 'wb') as f:
                f.write(private_pem)
        public_pem = rsa.publickey().exportKey()
        if not os.path.exists(os.path.join(self.basePath, 'public.pem')):
            with open(os.path.join(self.basePath, 'public.pem'), 'wb') as f:
                f.write(public_pem)
        print("生成成功")

    def get_public_key(self):
        with open(os.path.join(self.basePath, 'public.pem'), 'rb') as f:
            key = f.read()
            return key

    def get_private_key(self):
        with open(os.path.join(self.basePath, 'private.pem'), 'rb') as f:
            key = f.read()
            return key

    def encrypt(self, str):  # 用公钥加密
        pubkey = RSA.import_key(self.get_public_key())
        original_text = str.encode('utf8')
        cipher = Cipher_pkcs1_v1_5.new(pubkey)
        cipher_text = base64.b64encode(cipher.encrypt(original_text)).decode()
        return cipher_text

    def decrypt(self, crypt_text):  # 用私钥解密
        try:
            privateKey = RSA.importKey(self.get_private_key())
            cipher = Cipher_pkcs1_v1_5.new(privateKey)
            text = cipher.decrypt(base64.b64decode(crypt_text), None).decode()
            return text
        except Exception as e:
            raise Exception("token 无效")

    def signature(self, str):  # 公钥签名
        public_key = RSA.importKey(self.get_public_key())
        hash_obj = SHA1.new(bytearray(str, encoding='utf-8'))
        signature = base64.b64encode(pkcs1_15.new(
            public_key).sign(hash_obj)).decode()
        return signature
