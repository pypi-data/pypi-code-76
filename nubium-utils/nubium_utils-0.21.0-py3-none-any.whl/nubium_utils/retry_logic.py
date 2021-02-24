import os


def produce_retry_message(message, producer, error):
    """
    Produces a message to the correct retry topic with an updated header

    The message header should contain a `kafka_retry_count` field,
    which is an integer representation of how many times the message has
    been tried for the current topic.
    If greater than the allowed maximum, produces to the retry topic.
    If less than the allowed maximum, produces to the current topic.
    """

    message_headers = dict(message.headers())
    kafka_retry_count = int(message_headers.get('kafka_retry_count', '0'))

    # If less than the retry max, produce onto the original topic
    if kafka_retry_count < int(os.environ['RETRY_COUNT_MAX']):
        message_headers['kafka_retry_count'] = str(kafka_retry_count + 1)
        producer.produce(
            topic=os.environ['CONSUME_TOPICS'],
            value=message.value(),
            key=message.key(),
            headers=message_headers
        )

    # Otherwise, reset the retry count and produce to the retry topic
    else:
        message_headers['kafka_retry_count'] = '0'
        producer.produce(
            topic=os.environ['PRODUCE_RETRY_TOPICS'],
            value=message.value(),
            key=message.key(),
            headers=message_headers
        )
