import logging
import os
import time
import datetime

from .custom_exceptions import NoMessageError, ConsumeMessageError
from .metrics import MetricsManager

LOGGER = logging.getLogger('nubium-utils')


def _wait_until_message_time(message):
    """
    Wait until the message's timestamp + the deployments offset before handling

    :param message: the kafka message being handled
    :return: None
    """
    message_time = message.timestamp()[1] + (
            int(os.environ['TIMESTAMP_OFFSET_MINUTES']) * 60
    )

    # Divide to get in normal datetime format, since it's milliseconds
    message_time /= 1000

    wait_time = message_time - datetime.datetime.timestamp(
        datetime.datetime.utcnow())

    if wait_time > 0:
        time.sleep(wait_time)


def consume_message(consumer, timeout, monitor: MetricsManager):
    """
    Consumes a message from the broker while handling errors and waiting if necessary

    Polls the broker for a message using the given timeout.
    If there are no messages to consume, either because None is returned
    or the message error is the no messages error,
    raises a NoMessageError.

    If the message is returned with a breaking error,
    raises a ConsumeMessageError.

    If the message is valid, waits until the message's timestamp plus
    the current process's time offset before handling the message.
    This allows retry deployments to wait in a non-blocking fashion

    If the message is valid, then the message is returned
    """

    message = consumer.poll(timeout)

    if message is None:
        LOGGER.info("No messages to consume")
        raise NoMessageError("No messages to consume")

    try:
        guid = [item[1] for item in message.headers() if item[0] == 'guid'][0].decode()
        LOGGER.info(f"Message consumed: {guid}")
    except AttributeError:
        if "object has no attribute 'headers'" in str(message.error()):
            LOGGER.info("Message consumed. No headers, so no guid is available to log.")
    except TypeError:
        LOGGER.info("Message consumed. Headers are None, so no guid is available to log.")
    except IndexError:
        LOGGER.info("Message consumed. Headers found, but no guid is available to log.")

    # If message is None, it can mean that the poll operation timed out,
    # or that there are no more messages to consume

    if message.error():
        if "Broker: No more messages" in str(message.error()):
            LOGGER.warning("Consumer error: %s", message.error())
            raise NoMessageError(message.error())
        else:
            raise ConsumeMessageError(message.error())

    # Wait until message time if using a retry process
    _wait_until_message_time(message)

    # Increment the metric for consumed messages by one
    monitor.inc_messages_consumed(1)

    return message


