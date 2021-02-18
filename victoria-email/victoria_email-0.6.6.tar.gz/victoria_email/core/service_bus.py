"""service_bus

This module implements various functionality related to Azure Service Bus.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import logging
from typing import List
from os.path import join
import pickle

from azure.servicebus import ServiceBusClient
from azure.servicebus import Message
from azure.servicebus import ReceiveSettleMode


def get_all_dead_letter_ids(queue_str: str,
                            client: ServiceBusClient) -> List[str]:
    """Get a list of all message IDs in the dead letter queue of a given
    queue.

    Args:
        queue_str: The name of the queue.
        client: The service bus client.
    """
    logging.info(f"--> Getting dead letters from '{queue_str}'...")
    dead_letters = []
    queue = client.get_queue(queue_str)
    with queue.get_deadletter_receiver(idle_timeout=0.2) as dead_letter_rx:
        dead_letters += dead_letter_rx.peek(count=9999)

    dead_letter_ids = []
    for msg in dead_letters:
        dead_letter_ids.append(msg.properties.message_id.decode("utf-8"))
    logging.info(
        f"    Finished scanning. {len(dead_letters)} dead letter(s) were found."
    )
    return dead_letter_ids


def connect(connection_str: str) -> ServiceBusClient:
    """Initiate a connection to a service bus with a connection string."""
    return ServiceBusClient.from_connection_string(connection_str)


def copy_message(msg: Message) -> Message:
    """Create a copy of the service bus message given."""
    msg_body = b''
    for b in msg.body:
        msg_body += b
    new_msg = Message(msg_body)
    new_msg.properties = msg.properties
    return new_msg


def store_message_in_vault(message: Message, vault_dir: str):
    """Store a message's body in the vault in the event of failure.

    Args:
        message (Message): The message to store.
        vault_dir (str): The path to the vault folder to store it in.
                         This is 'vault_dir/cluster_name/queue_name/'.
    """
    # get the path to the file
    vault_file_path = join(vault_dir,
                           message.properties.message_id.decode("utf-8"))

    # write the message body
    with open(vault_file_path, 'wb') as vault_file:
        body = b''
        for b in message.body:
            body += b
        vault_file.write(body)


def resend_dead_letters_from_queue(vault_dir: str, queue: str,
                                   client: ServiceBusClient) -> List[str]:
    """Scan a queue for dead letters, and resend found.

    If there are any errors resending, store the message body in the vault.

    Args:
        vault_dir (str): The root dir of the vault.
        queue (str): The name of the queue to scan.
        client (ServiceBusClient): The service bus client to use.

    Returns:
        List[str]: The list of transaction IDs that were resent.
    """
    logging.info(f"--> Getting dead letters from '{queue}'...")
    resent_ids = []
    queue = client.get_queue(queue)
    with queue.get_deadletter_receiver(idle_timeout=0.2) as dead_letter_rx:
        with queue.get_sender() as queue_sender:
            number_replayed = 0

            # receive the messages from the dead letter queue
            for msg in dead_letter_rx:
                message_id = msg.properties.message_id.decode('utf-8')

                # messages without a body are invalid, we should skip those
                if msg.body is None:
                    logging.warn(
                        f"\tMessage '{message_id}' did not have a body.")
                    msg.complete()
                    continue

                try:
                    # now attempt to replay the error
                    logging.info(
                        f"\tReplaying a dead letter ({message_id})...")
                    store_message_in_vault(msg, vault_dir)
                    to_send = copy_message(msg)
                    queue_sender.send(to_send)
                    number_replayed += 1
                    resent_ids.append(message_id)
                except:
                    # if we get any errors while replaying, make sure the message
                    # is abandoned, and kept on the dead letter queue
                    logging.error("--> An error occurred while processing a dead letter."\
                        " Abandoning the message.")
                    msg.abandon()
                    return
                msg.complete()
            logging.info(
                f"    Finished scanning. {number_replayed} dead letter(s) were found and replayed."
            )
    return resent_ids
