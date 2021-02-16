import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
logger = logging.getLogger(__name__)


class DecryptEncrypt:
    def __init__(self):
        pass

    def encrypt_secret(self, secret, vault_name, keyid, subscription_id, region):
        logger.info("secret to encrypt: {0}" .format(secret))
        logger.info("keyid: {0}" .format(keyid))
        logger.info("Azure subscription id: {0}" .format(subscription_id))
        logger.info("Azure region: {0}" .format(region))
        # https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity#defaultazurecredential
        vault_url = "https://{0}.vault.azure.net/".format(vault_name)
        logger.info("vault url: " .format(vault_url))
        byte_literal_value = secret.encode()  # convert string to byte literal
        credential = DefaultAzureCredential()
        key_client = KeyClient(vault_url=vault_url, credential=credential)
        key = key_client.get_key(keyid)
        crypto_client = CryptographyClient(key, credential=credential)
        # the result holds the ciphertext and identifies the encryption key and algorithm used
        result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, byte_literal_value)
        ciphertext = result.ciphertext
        print("-" * 50)
        print("ciphertext: {0}" .format(ciphertext))
        print("result: {0}" .format(result.key_id))
        print(result.algorithm)
        print("-" * 50)

    def decrypt_secret(self, cipher_text, vault_name, keyid, subscription_id, region):
        logger.info("secret to decrypt: {0}".format(cipher_text))
        logger.info("keyid: {0}".format(keyid))
        logger.info("Azure subscription id: {0}".format(subscription_id))
        logger.info("Azure region: {0}".format(region))
        vault_url = "https://{0}.vault.azure.net/".format(vault_name)
        logger.info(vault_url)
        '''
        convert string to byte literal
        '''
        byte_literal_value = cipher_text.encode()
        '''
        You can use str.decode() with encoding as unicode-escape . 
        Then decode it back using the required encoding to get back your bytes array.
        '''
        byte_literal_value = byte_literal_value.decode('unicode-escape').encode('ISO-8859-1')
        credential = DefaultAzureCredential()
        key_client = KeyClient(vault_url=vault_url, credential=credential)
        key = key_client.get_key(keyid)
        crypto_client = CryptographyClient(key, credential=credential)

        decrypted = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, byte_literal_value)
        print("decrypted: ", decrypted.plaintext)


get_secret = DecryptEncrypt()
