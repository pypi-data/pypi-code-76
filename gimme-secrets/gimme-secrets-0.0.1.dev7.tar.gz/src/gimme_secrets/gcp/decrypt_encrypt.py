import logging
logger = logging.getLogger(__name__)


class DecryptEncrypt:
    def __init__(self):
        pass

    def encrypt_secret(self, secret, vault_name, keyid, subscription_id, region):
        logger.info("secret to encrypt: {0}" .format(secret))
        logger.info("keyid: {0}" .format(keyid))
        logger.info("GCP project id: {0}" .format(subscription_id))
        logger.info("GCP region: {0}" .format(region))

    def decrypt_secret(self, cipher_text, vault_name, keyid, subscription_id, region):
        logger.info("secret to decrypt: {0}".format(cipher_text))
        logger.info("keyid: {0}".format(keyid))
        logger.info("GCP Project id: {0}".format(subscription_id))
        logger.info("GCP region: {0}".format(region))


get_secret = DecryptEncrypt()

# if __name__ == "__main__":
#     get_secret.encrypt_secret('text', env, kms_keyid, account, region)

