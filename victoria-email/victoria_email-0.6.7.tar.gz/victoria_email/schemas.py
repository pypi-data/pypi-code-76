"""schemas

Marshmallow schemas for the email plugin.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID
from typing import List, Dict

from marshmallow import Schema, fields, post_load, validate
from victoria.encryption.schemas import EncryptionEnvelopeSchema, EncryptionEnvelope

from .core.blob_storage import CONNECTION_STR, get_blob_properties
from .core.util import get_random_items
from .core.config import MailToilConfigSchema, MailToilConfig


class Load:
    def __init__(self, distribution: List[Dict] = None, attachment_count: List[int] = None):
        self.distribution = distribution
        self.attachment_count = attachment_count


class Function:
    def __init__(self, function: str, mail_send_function_code: str):
        self.function = function
        self.mail_send_function_code = mail_send_function_code


class DistributionSchema(Schema):
    file = fields.Str(required=True)
    weight = fields.Float(required=True)

    @post_load
    def make_config(self, data, **kwargs):
        return Distribution(**data)


class FunctionSchema(Schema):
    function = fields.Str(required=True)
    mail_send_function_code = fields.Str(required=True)

    @post_load
    def make_config(self, data, **kwargs):
        return Function(**data)

    def __str__(self):
        return f'{self.function}'


class LoadSchema(Schema):
    distribution = fields.List(fields.Nested(DistributionSchema))
    attachment_count = fields.List(fields.Int())

    @post_load
    def make_config(self, data, **kwargs):
        return Load(**data)


class LoadTestConfigSchema(Schema):
    """Marshmallow schema for the load testing config section."""
    mail_send_function_endpoints = fields.List(fields.Nested(FunctionSchema), required=True)
    # mail_send_function_code = fields.Str(required=True, allow_none=False)
    tenant_ids = fields.List(fields.UUID(allow_none=False), required=False)
    timeout = fields.Float(required=False, allow_none=False, missing=1.0)
    load = fields.Nested(LoadSchema, required=False)
    attachments = fields.Dict(keys=fields.Str(),
                              values=fields.Nested(
                                EncryptionEnvelopeSchema,
                                allow_none=False),
                              required=False)

    @post_load
    def make_config(self, data, **kwargs):
        return LoadTestConfig(**data)


@dataclass
class LoadTestConfig:
    """The config of the load tester.

    Attributes:
        mail_send_function_endpoints: The HTTP endpoints of the going-postal backend.
        tenant_ids: The tenant ID(s) to attach to the sent tests.
        timeout: The SMTP sending timeout to use.
        load:
        attachments: (fields.Dict[str, str]): mapping of storage_connection_strings with their respective value
    """
    # mail_send_function_code: str
    timeout: float
    mail_send_function_endpoints: field(default_factory=Function)
    load: Load = field(default_factory=Load)
    tenant_ids: List[UUID] = field(default_factory=list)
    attachments: Dict[str, EncryptionEnvelope] = field(default_factory=dict)


class EmailConfigSchema(Schema):
    """Marshmallow schema for the email plugin config."""
    load_test = fields.Nested(LoadTestConfigSchema,
                              required=False,
                              allow_none=True,
                              missing=None)
    mail_toil = fields.Nested(MailToilConfigSchema,
                              required=False,
                              allow_none=True,
                              missing=None)

    @post_load
    def make_config(self, data, **kwargs):
        return EmailConfig(**data)


@dataclass
class EmailConfig:
    """The email plugin config.

    Attributes:
        load_test: The config for the load testing command.
        mail_toil: The config for the mail toil commands.
    """
    load_test: LoadTestConfig
    mail_toil: Optional[MailToilConfig]


class Distribution:
    def __init__(self, file: str, weight: float):
        self.file = file
        self.weight = weight

    @classmethod
    def get_random_distributions(cls, load_test_config: LoadTestConfig, plugin_cfg: EmailConfig):
        encryption_provider = plugin_cfg.victoria_config.get_encryption()
        conn_str = encryption_provider.decrypt_str(load_test_config.attachments.get('storage_connection_strings')) \
            if load_test_config.attachments \
            else CONNECTION_STR

        properties = get_blob_properties('fileattachments', conn_str)
        return [cls(attachment.name, attachment.size) for attachment in
                get_random_items(properties, count=100)]
