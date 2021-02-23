import ast
import json
import logging
import threading
from inspect import signature

from pika import BlockingConnection, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from snacks import APP
from snacks.rabbit_config import RabbitConfig

__all__ = ('Rabbit',)

log = logging.getLogger(APP)


class Rabbit:
    """A class to interface with RabbitMQ."""

    def __init__(self, rabbit_config: RabbitConfig) -> None:
        self.config = rabbit_config

    # TODO Add support for return values.
    def publish(self, msg: any, routing_key: str) -> None:
        """Publish message to a rabbit queue with the given routing key.

        :param msg: The message to publish.
        :param routing_key: The routing key.
        """
        log.debug('Publishing key={} msg={}', routing_key, msg)
        mq_conn = BlockingConnection(self.config.params)
        channel: BlockingChannel = mq_conn.channel()
        channel.basic_publish(
            exchange=self.config.exchange_name,
            routing_key=routing_key,
            body=str(msg).encode()
        )

    # TODO Add support for decorated function to return values.
    def listener(self, queues: list[str]) -> callable:
        """Decorate a function to make it a rabbit consumer.

        The decorated function can have as parameters, the message body,
        the method, the properties, or no parameters.

        :param queues: The queues to consume from.
        :return: Function decorated to be a rabbit consumer.
        """
        mq_conn = BlockingConnection(self.config.params)
        channel = mq_conn.channel()

        def wrapper(fun: callable) -> None:
            [_listen(channel, queue, fun) for queue in queues]

        return wrapper


def _listen(channel: BlockingChannel,
            queue: str,
            fun: callable) -> callable:
    def callback(ch: BlockingChannel,
                 method: Basic.Deliver,
                 properties: BasicProperties,
                 body: bytes) -> None:
        log.debug('{} received {}', queue, body)
        sig = signature(fun)
        kwargs: dict[str, any] = {}
        for name, param in sig.parameters.items():
            if name == 'self':
                continue
            if param.annotation == BlockingChannel:
                kwargs[name] = ch
            elif param.annotation == method:
                kwargs[name] = method
            elif param.annotation == BasicProperties:
                kwargs[name] = properties
            elif param.annotation == str:
                kwargs[name] = body.decode('utf-8')
            elif param.annotation in {list, tuple, set, dict}:
                kwargs[name] = ast.literal_eval(body.decode('UTF-8'))
            elif param.annotation == bytes:
                kwargs[name] = body
            elif param.annotation in {int, float}:
                kwargs[name] = param.annotation(body)
            else:
                try:
                    kwargs[name] = param.annotation.from_dict(json.loads(body))
                except AttributeError:
                    try:
                        kwargs[name] = json.loads(body)
                    except json.decoder.JSONDecodeError:
                        kwargs[name] = body
        # noinspection PyBroadException
        try:
            return fun(**kwargs)
        except Exception as e:
            log.exception(msg=f'{type(e).__name__}: {e}', exc_info=e)

    channel.basic_consume(
        queue=queue,
        auto_ack=True,
        on_message_callback=callback
    )
    thread = threading.Thread(target=_consume, args=(channel,))
    thread.daemon = True
    thread.start()
    return fun


def _consume(channel: BlockingChannel) -> None:
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        channel.close()
