"""replay_deadletters

The functionality for the replay command from MailToil is implemented here.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import logging
import logging.config
import os
from os.path import join
from typing import List

from .core import config
from .core import service_bus
from .schemas import EmailConfig


def create_vault(queues: List[str], cluster: str, vault_dir: str) -> None:
    """Create the vault. The vault is used to store message bodies in the event
    of a failure when replaying them. This ensures you don't lose messages.

    The vault structure is:
    vault-directory
        cluster0
            queue0
            queue1
            ...
            queueN
        cluster1
        ...
        clusterN

    Args:
        queues (List[str]): The list of queues to create vaults for.
        cluster (str): The cluster to create a vault for.
        vault_dir (str): The root directory of the vault.
    """
    logging.info(f"Creating vault for {cluster}...")

    # for each queue, create a directory
    for queue in queues:
        try:
            os.makedirs(join(vault_dir, cluster, queue))
        except FileExistsError:
            # if it already exists do nothing
            pass


def replay(cfg: config.MailToilConfig, cluster: str, plugin_cfg: EmailConfig):
    """Perform the mailtoil replay functionality.

    Args:
        cfg: The mail toil config.
        cluster: The cluster to replay from.
        plugin_cfg: The email plugin config.
    """
    encryption_provider = plugin_cfg.victoria_config.get_encryption()
    service_bus_conn_str = encryption_provider.decrypt_str(
        cfg.get_service_bus_connection_str(cluster))
    #service_bus_conn_str = cfg.get_service_bus_connection_str(cluster)

    if service_bus_conn_str is None:
        raise SystemExit(1)

    # create the vault
    create_vault(cfg.queues, cluster, cfg.vault_dir)

    # connect to the service bus
    client = service_bus.connect(service_bus_conn_str)

    # scan for and resend dead letters on each queue in the config
    resent_transaction_ids = []
    logging.info(f"Scanning queues on '{cluster}' for dead letters...")
    for queue in cfg.queues:
        vault_dir = join(cfg.vault_dir, cluster, queue)
        resent = service_bus.resend_dead_letters_from_queue(
            vault_dir, queue, client)
        resent_transaction_ids += resent

    # print resent transaction IDs so an SRE can go and check if they were sent
    logging.info(f"{len(resent_transaction_ids)} dead letters were resent." \
        " Please check if the following transaction IDs were successfully relayed.")
    for tx_id in resent_transaction_ids:
        logging.info(tx_id)