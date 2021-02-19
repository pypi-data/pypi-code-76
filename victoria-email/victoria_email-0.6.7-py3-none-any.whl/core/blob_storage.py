from io import BytesIO
import json
import logging
import os

from azure.common import AzureMissingResourceHttpError
from azure.core.paging import ItemPaged
from azure.storage.blob import BlobServiceClient, BlobProperties, ContainerClient

# sometimes it's in different places in the blob storage container, not
# sure what causes this or even if it's still an issue but in November-ish 2019
# we had reconstructions that weren't working due to Received/MimeMessage not
# being present - so we always need to check for both of these
MIME_BLOB_NAMES = [
    "Received/MimeMessage",
    "MessageInspectionQueue/Glasswall.FileTrust.Messaging.ReceivedMessage.json"
]
"""The name of the blob within the container that contains the MIME message."""

CONNECTION_STR = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')


def connect(connection_str: str) -> BlobServiceClient:
    """Connect to the Azure Blob Storage account using a StorageAccount.

    Args:
        storage_account (StorageAccount): The storage account creds to use.

    Returns:
        BlobServiceClient: The blob service to use.
    """
    return BlobServiceClient.from_connection_string(connection_str.replace(';;', ';'))


def get_mime_message(transaction_id: str,
                     blob_service: BlobServiceClient) -> str:
    """Get the MIME message received from a transaction ID.

    Args:
        transaction_id (str): The transaction ID to use to get the message.
        blob_service (BlockBlobService): The service to use to get the message.

    Returns:
        str: The MIME message.
    """
    for blob_name in MIME_BLOB_NAMES:
        try:
            logging.debug(transaction_id, blob_name)
            blob_client = blob_service.get_blob_client(transaction_id.lower(),
                                                       blob_name)
            blob = blob_client.download_blob()
            blob_content = BytesIO()
            blob_content.write(blob.readall())
            blob_content = blob_content.getvalue().decode('utf-8')

            if blob_name.endswith(".json"):
                mime_json = json.loads(blob_content)
                return mime_json["receivedMimeMessage"]
            else:
                return blob_content
        except AzureMissingResourceHttpError:
            # this is pure filth, but some of the blobs are in messed up formats
            # and we need to try multiple times to get the MIME message
            continue

    logging.error(
        f"Transaction ID '{transaction_id}' not found in blob storage")
    return None


def get_container(container_name: str, connection_str: str) -> ContainerClient:
    return connect(connection_str).get_container_client(container_name)


def get_blob_properties(container_name: str, connection_str: str) -> ItemPaged[BlobProperties]:
    return get_container(container_name, connection_str).list_blobs()
