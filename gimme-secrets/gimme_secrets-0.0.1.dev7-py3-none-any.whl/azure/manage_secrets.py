# from .decrypt_encrypt import *
# import os
from azure.keyvault.secrets import SecretClient
# from azure.identity import DefaultAzureCredential
import logging
from azure.identity import DefaultAzureCredential
# from azure.keyvault.keys import KeyClient
# from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

logger = logging.getLogger(__name__)


class GetValuesFromLocker:
    def __init__(self):
        pass

    def get_value_from_secrets(self, secretName, vault_name, subscription_id):
        vault_url = "https://{0}.vault.azure.net/".format(vault_name)
        credential = DefaultAzureCredential()
        key_client = SecretClient(vault_url=vault_url, credential=credential)
        retrieved_secret = key_client.get_secret(secretName)
        print("-" * 50, "\nSecret Name: {0}\nSecret: {1}\nVault Name: {2}\n" .format(secretName, retrieved_secret.value, vault_name), "-" * 50)

    def put_value_from_secrets(self, secretName, secretValue, vault_name, subscription_id):
        vault_url = "https://{0}.vault.azure.net/".format(vault_name)
        print("vault url: {0}"  .format(vault_url))
        credential = DefaultAzureCredential()
        key_client = SecretClient(vault_url=vault_url, credential=credential)
        try:
            key_client.set_secret(secretName, secretValue)
            print("value has been put in key vault")
        except:
            print("unable to put value in key vault")


manage_values = GetValuesFromLocker()
