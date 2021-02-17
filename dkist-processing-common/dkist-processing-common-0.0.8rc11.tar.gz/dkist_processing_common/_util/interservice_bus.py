import json
from collections import defaultdict
from os import environ
from uuid import uuid4

from talus.message import message_class

from dkist_processing_common._util.config import get_mesh_config

# Environment variable indicating how to connect to dependencies on the service mesh
MESH_CONFIG = get_mesh_config()

RABBITMQ_CONFIG = {
    "rabbitmq_host": MESH_CONFIG["interservice-bus"]["mesh_address"],
    "rabbitmq_port": MESH_CONFIG["interservice-bus"]["mesh_port"],
    "rabbitmq_user": environ.get("ISB_USERNAME"),
    "rabbitmq_pass": environ.get("ISB_PASSWORD"),
}


@message_class(routing_key="catalog.frame.m", queues=["catalog.frame.q"])
class CatalogFrameMessage:
    """
    Class to hold the catalog_frame_message to be sent to RabbitMQ
    """

    objectName: str = "default_object_name"
    conversationId: str = str(uuid4().hex)
    bucket: str = "data"
    incrementDatasetCatalogReceiptCount: bool = True


@message_class(routing_key="catalog.object.m", queues=["catalog.object.q"])
class CatalogObjectMessage:
    """
    Class to hold the catalog_object_message to be sent to RabbitMQ
    """

    objectType: str
    objectName: str = "default_object_name"
    conversationId: str = str(uuid4().hex)
    bucket: str = "data"
    groupId: str = "default_group_id"
    groupName: str = "DATASET"
    incrementDatasetCatalogReceiptCount: bool = True
