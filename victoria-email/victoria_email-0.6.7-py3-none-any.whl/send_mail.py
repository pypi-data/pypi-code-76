"""send_mail

Implements the mailsend.py functionality in the Victoria plugin.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from __future__ import annotations
from datetime import datetime
import logging
from os import path
from typing import List
import uuid

from marshmallow import Schema, fields, post_load, validate, ValidationError, EXCLUDE
from sremail import address, message, smtp
import yaml


class ManifestSchema(Schema):
    """Marshmallow schema for an email manifest."""
    sender = address.AddressField(required=True, allow_none=False)
    to = fields.List(address.AddressField,
                     required=True,
                     validate=validate.Length(min=1),
                     allow_none=False)
    smtp_server = fields.String(required=True, allow_none=False)
    tenant_id = fields.UUID(required=True)
    port = fields.Int(missing=25, allow_none=False)
    attach = fields.List(fields.Str, missing=[], allow_none=False)

    @post_load
    def make_manifest(self, data, **kwargs):
        return Manifest(**data)


MANIFEST_SCHEMA = ManifestSchema(unknown=EXCLUDE)
"""A module-wide instance of ManifestSchema to use when
loading a Manifest."""


class Manifest:
    """A manifest is a description of an email we want to send.

    Attributes:
        sender: The email address sending the email.
        to: The list of emails to send the email to.
        smtp_server: The SMTP server to send the email to.
        tenant_id: The FileTrust tenant ID to send the email with.
        port: The port on the SMTP server to connect via.
        attach: The list of files to attach.
    """
    def __init__(self, sender: address.Address, to: List[address.AddressField],
                 smtp_server: str, tenant_id: uuid.UUID, port: int,
                 attach: List[str]) -> None:
        self.sender = sender
        self.to = to
        self.smtp_server = smtp_server
        self.tenant_id = tenant_id
        self.port = port
        self.attach = attach

    @classmethod
    def load(cls, filepath: str) -> Manifest:
        """Create a Manifest from a YAML file on disk.

        Args:
            filepath (str): The path to the YAML file to use.
        """
        # try and load, print any errors if they occur
        with open(filepath, "r") as manifest_file:
            logging.info(f"Loading manifest file: {filepath}")
            manifest_yaml = yaml.safe_load(manifest_file)
            try:
                return MANIFEST_SCHEMA.load(manifest_yaml)
            except ValidationError as err:
                __print_validation_err(err, filepath)


def __print_validation_err(err: ValidationError, manifest_name: str) -> None:
    """Internal function used for logging a validation error in the Manifest
    Schema.

    Args:
        err (ValidationError): The error to log.
        manifest_name (str): A human-readable identifier for the manifest.
    """
    # build up a string for each error
    log_str = []
    log_str.append(f"Error loading manifest '{manifest_name}':")
    for field_name, err_msgs in err.messages.items():
        log_str.append(f"{field_name}: {err_msgs}")

    # log the joined up string, and exit with an error
    logging.critical(" ".join(log_str))
    raise SystemExit(1)


def send_manifest(manifest: Manifest) -> None:
    """Send a given manifest's email to its target.

    Args:
        manifest: The manifest to send.
    """
    msg = message.Message(to=manifest.to,
                          from_addresses=[manifest.sender],
                          date=datetime.now())
    for attachment in manifest.attach:
        if not path.exists(attachment):
            logging.error(f"Unable to attach {attachment}, file did not exist")
            return
        logging.info(f"Attaching {attachment}...")
        msg.attach(attachment)
    msg.headers["X-FileTrust-Tenant"] = str(manifest.tenant_id)

    smtp_url = f"{manifest.smtp_server}:{manifest.port}"
    logging.info(f"Sending manifest to: {smtp_url}...")
    smtp.send(msg, smtp_url)