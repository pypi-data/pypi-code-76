"""reconstruct_mail

Contains the functionality for the mail reconstruction portion of the
mailtoil scripts.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import datetime
import email
import logging
from os import makedirs
from typing import List, Optional

from .core import blob_storage
from .core import config
from .core import mail_reconstruction
from .core import service_bus
from .schemas import EmailConfig


def create_output_dir(output_dir: str) -> None:
    """Create the output directory."""
    try:
        makedirs(output_dir)
    except FileExistsError:
        # don't do anything if it already existed
        pass


def get_dead_letters_from_service_bus(cluster: str, cfg: config.MailToilConfig,
                                      conn_str: str) -> List[str]:
    """Get the list of dead letter IDs from the service bus."""
    # connect to the service bus for the cluster

    sb_client = service_bus.connect(
        cfg.get_service_bus_connection_str(cluster))

    # scan for dead letters to get IDs to cross reference in blob storage
    transaction_ids = []
    logging.info(f"Scanning queues on '{cluster}' for dead letters...")
    for queue in cfg.queues:
        dead_letters = service_bus.get_all_dead_letter_ids(queue, sb_client)
        for dead_letter in dead_letters:
            logging.info(f"\tFound dead letter '{dead_letter}'")
        transaction_ids += dead_letters
    logging.info(f"Found {len(transaction_ids)} dead letter(s) on '{cluster}'")
    return transaction_ids


def reconstruct(cfg: config.MailToilConfig, cluster: str, output_dir: str,
                transaction_ids: List[str], anonymise: bool,
                plugin_cfg: EmailConfig) -> None:
    """Perform the reconstruct functionality.

    Args:
        cfg: The mail toil config.
        cluster: The cluster to grab transactions from.
        output_dir: Where to write the reconstructed mail to.
        transaction_ids: The tx IDs to reconstruct.
        anonymise: Whether we should anonymise.
        plugin_cfg: The email plugin config object.
    """
    encryption_provider = plugin_cfg.victoria_config.get_encryption()
    storage_conn_str = encryption_provider.decrypt_str(
        cfg.get_storage_account(cluster))
    #storage_conn_str = cfg.get_storage_account(cluster)
    if storage_conn_str is None:
        raise SystemExit(1)

    create_output_dir(output_dir)

    # if transaction IDs weren't given then get them from dead letters
    # instead
    if len(transaction_ids) == 0:
        service_bus_conn_str = encryption_provider.decrypt_str(
            cfg.get_service_bus_connection_str(cluster))
        #service_bus_conn_str = cfg.get_service_bus_connection_str(cluster)
        if service_bus_conn_str is None:
            raise SystemExit(1)
        transaction_ids = get_dead_letters_from_service_bus(
            cluster, cfg, service_bus_conn_str)

    # now grab the MIME messages of these transactions and reconstruct them
    logging.info(f"Connecting to blob storage for '{cluster}'...")
    blob_client = blob_storage.connect(storage_conn_str)

    for transaction_id in transaction_ids:
        mime_msg = blob_storage.get_mime_message(transaction_id, blob_client)
        if mime_msg is not None:
            mail_reconstruction.process_mime_message(mime_msg, transaction_id,
                                                     output_dir, anonymise)
