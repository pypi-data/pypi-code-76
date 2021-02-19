"""config.py

Config is used for loading the YAML config file used with the script.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>

Date:
    2019-09-12
"""
import logging
from os.path import basename
from typing import Dict, List

from marshmallow import Schema, fields, post_load, EXCLUDE, ValidationError
from victoria.encryption.schemas import EncryptionEnvelopeSchema, EncryptionEnvelope
import yaml


class MailToilConfigSchema(Schema):
    """ConfigSchema is a marshmallow schema used for validating loaded configs.

    Fields:
        service_bus_connection_strings (fields.Dict[str, EncryptionEnvelope]): Mapping of cluster names to service bus connection strings.
        queues (fields.List[str]): List of queue names to search for dead letters.
        storage_connection_strings (fields.Dict[str, EncryptionEnvelope]): Mapping of cluster names to storage accounts.
        vault_dir (fields.Str): The path to the vault.
    """
    service_bus_connection_strings = fields.Dict(keys=fields.Str(),
                                                 values=fields.Nested(
                                                     EncryptionEnvelopeSchema,
                                                     allow_none=False),
                                                 required=True)
    queues = fields.List(fields.Str(), required=True)
    storage_accounts = fields.Dict(keys=fields.Str(),
                                   values=fields.Nested(
                                        EncryptionEnvelopeSchema,
                                        allow_none=False),
                                   required=True)
    vault_dir = fields.Str(required=True)

    @post_load
    def make_config(self, data, **kwargs):
        """Callback used by marshmallow after loading object. We're using it here
        to create an instance of Config after loading the data."""
        return MailToilConfig(**data)


CONFIG_SCHEMA = MailToilConfigSchema(unknown=EXCLUDE)
"""Instance of ConfigSchema to use for validation."""


class MailToilConfig:
    """Config is used to store mailreconstruction config.

    Attributes:
        service_bus_connection_strings (Dict[str, str]): Mapping of cluster names to service bus connection strings.
        queues (List[str]): List of queue names to search for dead letters.
        storage_connection_strings (Dict[str, str]): Mapping of cluster names to storage account connection strings.
        vault_dir (str): The path to the vault
    """
    def __init__(self,
                 service_bus_connection_strings: Dict[str, EncryptionEnvelope],
                 queues: List[str], storage_accounts: Dict[str, EncryptionEnvelope],
                 vault_dir: str) -> None:
        self.service_bus_connection_strings = service_bus_connection_strings
        self.queues = queues
        self.storage_accounts = storage_accounts
        self.vault_dir = vault_dir

    def get_service_bus_connection_str(self,
                                       cluster: str) -> EncryptionEnvelope:
        """Try and get a service bus connection string for a cluster.

        Args:
            cluster (str): The cluster name. Should be as defined in config file.

        Returns:
            EncryptionEnvelope: The encrypted service bus connection string.

        Raises:
            ValueError: if the cluster name wasn't found in the config.
        """
        if not self.service_bus_connection_strings.get(cluster):
            raise ValueError(
                f"Couldn't find service bus connection string for cluster '{cluster}'"
            )
        return self.service_bus_connection_strings[cluster]

    def get_storage_account(self, cluster: str) -> EncryptionEnvelope:
        """Try and get a storage connection string for a cluster.

        Args:
            cluster (str): The cluster name. Should be as defined in config file.

        Returns:
            EncryptionEnvelope: The encrypted storage connection string.

        Raises:
            ValueError: if the cluster name wasn't found in the config.
        """
        if not self.storage_accounts.get(cluster):
            raise ValueError(
                f"Couldn't find storage account for cluster '{cluster}'")
        return self.storage_accounts[cluster]
