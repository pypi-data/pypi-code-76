import uuid
from os import environ
from pathlib import Path
from typing import List

from globus_sdk import ClientCredentialsAuthorizer
from globus_sdk import ConfidentialAppAuthClient
from globus_sdk import GlobusError
from globus_sdk import TransferClient
from globus_sdk import TransferData


def get_globus_transfer_client() -> TransferClient:
    confidential_client = ConfidentialAppAuthClient(
        client_id=environ.get("GLOBUS_CLIENT_ID"), client_secret=environ.get("GLOBUS_CLIENT_SECRET")
    )
    authorizer = ClientCredentialsAuthorizer(
        confidential_client, scopes="urn:globus:auth:scope:transfer.api.globus.org:all"
    )
    return TransferClient(authorizer=authorizer)


def create_transfer(tc, source_endpoint, destination_endpoint) -> TransferData:
    return TransferData(
        tc,
        source_endpoint,
        destination_endpoint,
        verify_checksum=True,
    )


def submit_globus_transfer(
    source_files: List[Path],
    destination_files: List[Path],
    source_endpoint: str,
    destination_endpoint: str,
):
    """
    Parse the lists of source and destination filepaths, and submit the transfer
    :param source_files: locations of the files to be transferred
    :param destination_files: locations those files will be transferred to
    :param source_endpoint: id of the source endpoint
    :param destination_endpoint: id of the destination endpoint
    """
    # Validate source and destination paths
    if len(source_files) != len(destination_files):
        raise ValueError(
            f"Number of source and destination files must be equal."
            f"{len(source_files)} source files and {len(destination_files)} destination files were provided."
        )

    # Validate endpoints
    uuid.UUID(source_endpoint)
    uuid.UUID(destination_endpoint)

    tc = get_globus_transfer_client()
    transfer = create_transfer(tc, source_endpoint, destination_endpoint)

    # Add files to transfer
    for i, file in enumerate(source_files):
        transfer.add_item(source_files[i], destination_files[i])

    # Submit transfer
    transfer_result = tc.submit_transfer(transfer)
    globus_task_id = transfer_result["task_id"]
    while not tc.task_wait(task_id=globus_task_id, polling_interval=60):
        for event in tc.task_event_list(task_id=globus_task_id, num_results=None):
            if event["is_error"]:
                tc.cancel_task(task_id=globus_task_id)
                raise GlobusError(
                    f"Transfer unsuccessful: {event['description']=}, {event['details']=}"
                )
