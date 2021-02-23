from enum import Enum
from typing import Type

import msgpack
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.timezone import now
from kombu import Exchange, Connection, Producer
from rest_framework.serializers import BaseSerializer


class EventType(Enum):
    created = 'created'
    changed = 'changed'
    deleted = 'deleted'
    restored = 'restored'


class BasicPublisher:
    """ Object used for publishing.
    """

    def __init__(self, exchange_name: str, site: Site):
        """ Creates a new instance of BasicPublisher.
        If connection or channel are not defined, they will be initialized
        automatically from the global publish connection and channel objects.

        :param exchange_name:  Name of the exchange this publisher should publish to.
        """
        self.exchange_name = exchange_name
        self.site = site

    def exchange(self, exchange_type='topic'):
        """ Creates an exchange
        """
        exchange = Exchange(self.exchange_name, type=exchange_type, durable=True)
        return exchange

    def get_identity(self, data: dict) -> str:
        return data['href']

    def serializer_context(self) -> dict:
        """ Simulates a request context sot hat our serializers can operate properly.

        :param site_id: Optional parameter (but should generally
        :return: A single-key dictionary containing 'request' with a simulated request object.
        """
        # this is a terrible hack to make the requests still work from the CLI.
        from rest_framework.request import Request, HttpRequest

        class SimulatedHTTPRequest(HttpRequest):
            def _get_scheme(self):
                return "https"

        req = SimulatedHTTPRequest()

        req.META = {
            'SERVER_NAME': self.site.domain,
            'SERVER_PORT': 443,
            'SCRIPT_NAME': settings.FORCE_SCRIPT_NAME
        }
        return {'request': Request(req)}

    def _publish(self, body: any, routing_key: str) -> None:
        exchange = self.exchange()
        with Connection(settings.BROKER_URL) as conn:
            with conn.channel() as channel:
                producer = Producer(channel)
                producer.publish(
                    body,
                    exchange=exchange,
                    declare=[exchange],
                    content_type='application/x-msgpack',
                    routing_key=routing_key,
                    retry=True,
                    retry_policy={
                        'interval_start': 0,
                        'interval_step': 2,
                        'interval_max': 30,
                        'max_retries': 30
                    }
                )


class EntityPublisher(BasicPublisher):
    def construct_message(self, data: dict, entity: str, event: EventType, identity=None) -> bytes:
        """ Construct the message to be sent.
        """
        message = {
            "event_time": now().isoformat(),
            "identity": identity or self.get_identity(data),
            "event": event.value,
            "entity": entity,
            "data": data
        }
        return msgpack.packb(message, use_bin_type=True)

    def publish(self,
                message: any,
                message_serializer: Type[BaseSerializer],
                event: EventType,
                entity: str,
                message_identity: any = None) -> None:
        """ Publish the message to RabbitMQ.
        """
        data = message_serializer(message, context=self.serializer_context()).data

        body = self.construct_message(
            data=data,
            entity=entity,
            event=event,
            identity=message_identity
        )

        routing_key = f'{entity}.{event.value}'
        self._publish(body, routing_key)
