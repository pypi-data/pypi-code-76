from typing import List
from typing import Union

from talus import DurableBlockingProducerWrapper

from dkist_processing_common._util.interservice_bus import CatalogFrameMessage
from dkist_processing_common._util.interservice_bus import CatalogObjectMessage
from dkist_processing_common._util.interservice_bus import RABBITMQ_CONFIG


def publish_messages(messages: List[Union[CatalogFrameMessage, CatalogObjectMessage]]):
    """
    Send all frame, movie, and object messages for downstream services
    :param messages: the messages to be sent
    """
    bindings = [message.binding() for message in messages]
    with DurableBlockingProducerWrapper(
        producer_queue_bindings=bindings,
        publish_exchange="master.direct.x",
        retry_tries=0,
        **RABBITMQ_CONFIG
    ) as producer:

        for message in messages:
            producer.publish_message(message)
