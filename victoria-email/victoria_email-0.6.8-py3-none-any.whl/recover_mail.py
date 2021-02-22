"""recover_mail

The functionality of the recover MailToil script is ported here.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import email
import logging
import logging.config
import os
from os.path import join
from typing import List
import smtplib

from .core import config, service_bus, blob_storage, mail_reconstruction
from .schemas import EmailConfig


def recover(cfg: config.MailToilConfig, cluster: str, file: str, transaction_id: str,
            smtp_addr: str, plugin_cfg: EmailConfig) -> None:
    """Perform the mailtoil recover functionality.

    Args:
        cfg: The mail toil config.
        cluster: The cluster to recover.
        file: The file path to the input tx ID txt file.
        transaction_id: Transaction Id.
        smtp_addr: The SMTP address to send to.
        plugin_cfg: The email plugin config object.
    """
    encryption_provider = plugin_cfg.victoria_config.get_encryption()

    storage_conn_str = encryption_provider.decrypt_str(
         cfg.get_storage_account(cluster))

    #storage_conn_str = cfg.get_storage_account(cluster)
    if storage_conn_str is None:
        raise SystemExit(1)

    # connect to blob
    blob_client = blob_storage.connect(storage_conn_str)

    tx_ids = []

    if file:
        with open(file, "r") as tx_id_file:
            for line in tx_id_file:
                tx_ids.append(line.strip())
    elif transaction_id:
        tx_ids.append(transaction_id)

    with smtplib.SMTP(smtp_addr) as smtp:
        for tx_id in tx_ids:
            mime_str = blob_storage.get_mime_message(tx_id, blob_client)
            print(f"Found MIME message for tx '{tx_id}'")
            preprocessed_msg = mail_reconstruction.preprocess_mime_message(
                mime_str).encode("utf-8")
            mime_msg = email.message_from_bytes(preprocessed_msg)
            smtp.send_message(mime_msg)
            print(f"Sent to: {mime_msg['To']}, from: {mime_msg['From']}")