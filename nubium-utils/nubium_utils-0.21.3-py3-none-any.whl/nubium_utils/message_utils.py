import logging

LOGGER = logging.getLogger('nubium-utils')

def success_headers(headers):
    """
    Updates headers for a message when a process succeeds

    Resets the kafka_retry_count to 0,
    or adds if it didn't originally exist
    """

    try:
        headers = dict(headers)
    except TypeError:
        headers = {}

    headers['kafka_retry_count'] = '0'
    return headers

def produce_message_callback(error, message):
    """
    Logs the returned message from the Broker after producing
    """
    LOGGER.debug('Callback for producing to the fail topic')
    if error:
        LOGGER.critical(error)
    if message:
        LOGGER.info(message)

def consume_message_callback(error, partitions):
    """
    Logs the info returned when a successful commit is performed
    """
    LOGGER.debug('Callback for a commit operation from the consumer')
    if error:
        LOGGER.critical(error)
    else:
        LOGGER.debug('No commit errors')
