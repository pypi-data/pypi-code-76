import base64
import boto3
import logging
from .switch_account import switch_role

logger = logging.getLogger(__name__)


class DecryptEncrypt:
    def __init__(self):
        pass

    def encrypt_secret(self, secret, kms_keyid, child_role_arn, region):
        self.region = region
        logger.info("child role arn: {0}" .format(child_role_arn))
        child_session = switch_role.switch_to_child_role(child_role_arn)
        kmsclient = child_session.client('kms', region_name=self.region)
        stuff = kmsclient.encrypt(KeyId=kms_keyid, Plaintext=secret)
        binary_encrypted = stuff[u'CiphertextBlob']
        encrypted_password = base64.b64encode(binary_encrypted)
        print("encrypted value: {0}" .format(encrypted_password.decode()))
        return encrypted_password.decode()

    def decrypt_secret(self, kms_keyid, child_role_arn, region, ciphertext):
        print("decrypting secret")
        self.region = region
        self.child_role_arn = child_role_arn
        child_session = switch_role.switch_to_child_role(child_role_arn)
        kmsclient = child_session.client('kms', region_name=self.region)
        binary_data = base64.b64decode(ciphertext)
        meta = kmsclient.decrypt(CiphertextBlob=binary_data)
        plaintext = meta[u'Plaintext']
        print("decrypted value: {0}" .format(plaintext.decode()))
        return plaintext.decode()


get_secret = DecryptEncrypt()
