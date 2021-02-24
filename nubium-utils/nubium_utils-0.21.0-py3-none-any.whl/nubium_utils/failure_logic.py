import os
import logging

from .message_utils import produce_message_callback

LOGGER = logging.getLogger('nubium-utils')


def produce_failure_message(message, producer):
    """
    Produces a message onto a deadletter queue
    """
    LOGGER.info('Producing message to deadletter queue')
    producer.produce(
        topic=os.environ['PRODUCE_FAILURE_TOPICS'],
        value=message.value(),
        key=message.key(),
        on_delivery=produce_message_callback
        )
