"""MQTT client for local Mosquitto broker.
"""
from atexit import register as on_exit
from logging import Logger, DEBUG
from json import dumps as json_dumpstr
from json import loads as json_loadstr
from json import JSONDecodeError
from os import getenv
from paho.mqtt.client import Client, MQTT_ERR_SUCCESS
from threading import enumerate as enumerate_threads
from time import time
from typing import Callable, Union

from utils.log import get_wrapping_logger

MQTT_HOST = getenv('MQTT_HOST') or 'isatiot'
MQTT_USERNAME = getenv('MQTT_USERNAME') #: or 'pnpdongle'
MQTT_PASS = getenv('MQTT_PASS') #: or 'isatFieldEdgeUltralite'

CONNECTION_RESULT_CODES = {
    0: 'MQTT_ERR_SUCCESS',
    1: 'MQTT_ERR_INCORRECT_PROTOCOL',
    2: 'MQTT_ERR_INVALID_CLIENT_ID',
    3: 'MQTT_ERR_SERVER_UNAVAILABLE',
    4: 'MQTT_ERR_BAD_USERNAME_PASSWORD',
    5: 'MQTT_ERR_UNAUTHORIZED',
}


class MqttError(Exception):
    pass


class MqttClient:
    """A customized MQTT client.

    Attributes:
        client_id: A unique client_id
        on_connect: A function called when the client connects to the broker
        on_disconnect: A function called when the client disconnects
        subscriptions: A dictionary of added subscriptions

    """
    def __init__(self,
                 client_id: str,
                 on_message: Callable[..., "tuple[str, object]"],
                 subscribe_default: Union[str, "list[str]"] = None,
                 on_connect: Callable = None,
                 on_disconnect: Callable = None,
                 logger: Logger = None):
        """Initializes a managed MQTT client.
        
        Args:
            client_id: The unique client ID
            on_message: The callback when subscribed messages are received
            subscribe_default: The default subscription(s) on re/connection
            logger: (optional) Logger

        """
        self._log = logger or get_wrapping_logger(name='mqtt', log_level=DEBUG)
        if not isinstance(client_id, str) or client_id == '':
            self._log.error('Invalid client_id')
            raise MqttError('Invalid client_id')
        if not callable(on_message):
            self._log.warning('No on_message specified')
        on_exit(self._cleanup)
        self.on_message = on_message
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.client_id = client_id
        self._mqtt = Client()
        self._mqtt_connected = False
        self._subscriptions = {}
        if subscribe_default:
            if not isinstance(subscribe_default, list):
                subscribe_default = [subscribe_default]
            for sub in subscribe_default:
                self.subscription_add(sub)
        self._connect()
    
    @property
    def client_id(self):
        return self._client_id
    
    @client_id.setter
    def client_id(self, id: str):
        try:
            if isinstance(int(id.split('_')[1]), int):
                # previously made unique, could be a bouncing MQTT connection
                id = id.split('_')[0]
        except (ValueError, IndexError):
            pass   #: new id will be made unique
        self._client_id = '{}_{}'.format(id, str(int(time())))

    @property
    def subscriptions(self) -> "list[str]":
        """The list of subscriptions.
        
        Use subscription_add or subscription_del to change the list.
        """
        return self._subscriptions

    def _cleanup(self):
        self._log.debug('Terminating MQTT connection')
        self._mqtt_on_disconnect(client=None, userdata='terminate', rc=0)
    
    def _connect(self):
        try:
            self._log.debug('Attempting MQTT broker connection to {} as {}'
                .format(MQTT_HOST, self._client_id))
            self._mqtt.reinitialise(client_id=self.client_id)
            self._mqtt.on_connect = self._mqtt_on_connect
            self._mqtt.on_disconnect = self._mqtt_on_disconnect
            self._mqtt.on_subscribe = self._mqtt_on_subscribe
            self._mqtt.on_message = self._mqtt_on_message
            if MQTT_USERNAME and MQTT_PASS:
                self._mqtt.username_pw_set(username=MQTT_USERNAME,
                                        password=MQTT_PASS)
            self._mqtt.connect(MQTT_HOST)
            threads_before = enumerate_threads()
            self._mqtt.loop_start()
            threads_after = enumerate_threads()
            for thread in threads_after:
                if thread in threads_before:
                    continue
                thread.name = 'MqttThread'
                break
        except Exception as e:
            raise MqttError('MQTT {}'.format(e))

    def _mqtt_on_connect(self, client, userdata, flags, rc):
        self._log.debug('MQTT broker connection result code: {} ({})'
            .format(rc, CONNECTION_RESULT_CODES[rc]))
        if rc == 0:
            self._log.info('MQTT connection to {}'.format(MQTT_HOST))
            if not self._mqtt_connected:
                for sub in self.subscriptions:
                    self._mqtt_subscribe(sub, self.subscriptions[sub]['qos'])
                self._mqtt_connected = True
            if self.on_connect:
                self.on_connect()
        else:
            self._log.error('MQTT connection result code {}'.format(rc))
    
    def _mqtt_subscribe(self, topic: str, qos: int = 0):
        self._log.debug('{} subscribing to {}'.format(self._client_id, topic))
        (result, mid) = self._mqtt.subscribe(topic=topic, qos=2)
        if result == MQTT_ERR_SUCCESS:
            self._subscriptions[topic]['mid'] = mid
        else:
            self._log.error('MQTT Error {} subscribing to {}'.format(
                result, topic))

    def _mqtt_unsubscribe(self, topic: str):
        self._log.debug('{} unsubscribing to {}'.format(self._client_id, topic))
        (result, mid) = self._mqtt.unsubscribe(topic)
        if result != MQTT_ERR_SUCCESS:
            self._log.error('MQTT Error {} unsubscribing to {}'.format(
                result, topic))

    def subscription_add(self, topic: str, qos: int = 0):
        """Adds a subscription to the client."""
        self._log.debug('Adding subscription {} qos={}'.format(topic, qos))
        self._subscriptions[topic] = {'qos': qos, 'mid': 0}
        if self._mqtt_connected:
            self._mqtt_subscribe(topic, qos)
        else:
            self._log.warning('MQTT not connected will subscribe later')

    def subscription_del(self, topic: str):
        """Removes a subscription to the client."""
        self._log.debug('Removing subscription {}'.format(topic))
        if topic in self._subscriptions:
            del self._subscriptions[topic]
        if self._mqtt_connected:
            self._mqtt_unsubscribe(topic)

    def _mqtt_on_disconnect(self, client, userdata, rc):
        if self.on_disconnect:
            self.on_disconnect()
        self._mqtt.loop_stop()
        self._mqtt.disconnect()
        if userdata != 'terminate':
            self._log.warning('MQTT broker disconnected: result code {} ({})'
                .format(rc, CONNECTION_RESULT_CODES[rc]))
            # get new unique ID to avoid bouncing connection
            self.client_id = self.client_id
            self._mqtt_connected = False
            self._connect()

    def _mqtt_on_subscribe(self, client, userdata, mid, granted_qos):
        self._log.debug('MQTT subscription message id: {}'.format(mid))
        for sub in self.subscriptions:
            if mid != self.subscriptions[sub]['mid']:
                self._log.error('Subscription failed message id={} expected {}'
                    .format(mid, self.subscriptions[sub]['mid']))
            else:
                self._log.info('Subscription to {} successful'.format(sub))

    def _mqtt_on_message(self, client, userdata, message):
        payload = message.payload.decode()
        try:
            payload = json_loadstr(payload)
        except JSONDecodeError as e:
            self._log.debug('MQTT message payload non-JSON ({})'.format(e))
        self._log.debug('MQTT received {} message: {}'.format(
            message.topic, payload))
        self.on_message(message.topic, payload)

    def publish(self, topic: str, message: str):
        """Publishes a message to a MQTT topic."""
        if not isinstance(message, str):
            message = json_dumpstr(message)
        self._log.info('MQTT publishing: {}/{}'.format(topic, message))
        (rc, mid) = self._mqtt.publish(topic=topic, payload=message, qos=2)
        del mid
        if rc != MQTT_ERR_SUCCESS:
            self._log.error('Publishing error {}'.format(rc))
            raise MqttError('Publishing error {}'.format(rc))
