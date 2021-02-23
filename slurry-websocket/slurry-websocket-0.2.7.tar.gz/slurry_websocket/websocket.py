"""Slurry websocket client."""
import logging

from slurry.sections.abc import Section
import trio
from trio_websocket import connect_websocket, connect_websocket_url
from trio_websocket import ConnectionTimeout, DisconnectionTimeout, HandshakeError, ConnectionClosed
import orjson
from wsproto.frame_protocol import CloseReason

log = logging.getLogger(__name__)

CONN_TIMEOUT = 60 # default connect & disconnect timeout, in seconds
MESSAGE_QUEUE_SIZE = 1
MAX_MESSAGE_SIZE = 2 ** 20 # 1 MiB
RECEIVE_BYTES = 4 * 2 ** 10 # 4 KiB

class Websocket(Section):
    """Create a WebSocket client connection to a URL.

    The websocket will connect when the pipeline is started.

    For more information, see the `trio-websocket documentation <https://trio-websocket.readthedocs.io/en/stable/api.html#connections`_.

    :param str url: A WebSocket URL, i.e. `ws:` or `wss:` URL scheme.
    :param ssl_context: Optional SSL context used for ``wss:`` URLs. A default
        SSL context is used for ``wss:`` if this argument is ``None``.
    :type ssl_context: ssl.SSLContext or None
    :param subprotocols: An iterable of strings representing preferred
        subprotocols.
    :param list[tuple[bytes,bytes]] extra_headers: A list of 2-tuples containing
        HTTP header key/value pairs to send with the connection request. Note
        that headers used by the WebSocket protocol (e.g.
        ``Sec-WebSocket-Accept``) will be overwritten.
    :param int message_queue_size: The maximum number of messages that will be
        buffered in the library's internal message queue.
    :param int max_message_size: The maximum message size as measured by
        ``len()``. If a message is received that is larger than this size,
        then the connection is closed with code 1009 (Message Too Big).
    :param float connect_timeout: The number of seconds to wait for the
        connection before timing out.
    :param float disconnect_timeout: The number of seconds to wait when closing
        the connection before timing out.
    :param bool parse_json: Serialise/deserialise websocket input and output automatically.

    :raises HandshakeError: for any networking error,
        client-side timeout (ConnectionTimeout, DisconnectionTimeout),
        or server rejection (ConnectionRejected) during handshakes.
    """
    def __init__(self, url, ssl_context=None, *, subprotocols=None,
        extra_headers=None,
        message_queue_size=MESSAGE_QUEUE_SIZE, max_message_size=MAX_MESSAGE_SIZE,
        connect_timeout=CONN_TIMEOUT, disconnect_timeout=CONN_TIMEOUT,
        parse_json=True):
        super().__init__()
        self.url = url
        self.ssl_context = ssl_context
        self.host = None
        self.port = None
        self.resource = None
        self.use_ssl = None
        self.subprotocols = subprotocols
        self.extra_headers = extra_headers
        self.message_queue_size = message_queue_size
        self.max_message_size = max_message_size
        self.connect_timeout = connect_timeout
        self.disconnect_timeout = disconnect_timeout
        self.parse_json = parse_json
        self._connection = None

    @classmethod
    def create(cls, host, port, resource, *, use_ssl, subprotocols=None,
        extra_headers=None,
        message_queue_size=MESSAGE_QUEUE_SIZE, max_message_size=MAX_MESSAGE_SIZE,
        connect_timeout=CONN_TIMEOUT, disconnect_timeout=CONN_TIMEOUT,
        parse_json=True):
        """Alternative client factory which creates a WebSocket client connection to a host/port.

        The websocket will connect when the pipeline is started.

        For more information, see the `trio-websocket documentation <https://trio-websocket.readthedocs.io/en/stable/api.html#connections`_.

        :param str host: The host to connect to.
        :param int port: The port to connect to.
        :param str resource: The resource, i.e. URL path.
        :param use_ssl: If this is an SSL context, then use that context. If this is
            ``True`` then use default SSL context. If this is ``False`` then disable
            SSL.
        :type use_ssl: bool or ssl.SSLContext
        :param subprotocols: An iterable of strings representing preferred
            subprotocols.
        :param list[tuple[bytes,bytes]] extra_headers: A list of 2-tuples containing
            HTTP header key/value pairs to send with the connection request. Note
            that headers used by the WebSocket protocol (e.g.
            ``Sec-WebSocket-Accept``) will be overwritten.
        :param int message_queue_size: The maximum number of messages that will be
            buffered in the library's internal message queue.
        :param int max_message_size: The maximum message size as measured by
            ``len()``. If a message is received that is larger than this size,
            then the connection is closed with code 1009 (Message Too Big).
        :param float connect_timeout: The number of seconds to wait for the
            connection before timing out.
        :param float disconnect_timeout: The number of seconds to wait when closing
            the connection before timing out.
        :param bool parse_json: Serialise/deserialise websocket input and output automatically.

        :raises HandshakeError: for any networking error,
            client-side timeout (ConnectionTimeout, DisconnectionTimeout),
            or server rejection (ConnectionRejected) during handshakes.
        """
        websocket = cls(None, None, subprotocols=subprotocols,
            extra_headers=extra_headers,
            message_queue_size=message_queue_size, max_message_size=max_message_size,
            connect_timeout=connect_timeout, disconnect_timeout=disconnect_timeout,
            parse_json=parse_json)
        websocket.host = host
        websocket.port = port
        websocket.resource = resource
        websocket.use_ssl = use_ssl

        return websocket

    async def pump(self, input, output):
        log.info('Slurry websocket starting.')
        async def send_task():
            send_message = self._connection.send_message
            async for message in input:
                await send_message(message)

        async def send_json_task():
            send_message = self._connection.send_message
            async for item in input:
                await send_message(orjson.dumps(item).decode())

        async with trio.open_nursery() as nursery:
            try:
                with trio.fail_after(self.connect_timeout):
                    if self.url:
                        self._connection = await connect_websocket_url(nursery,
                            self.url, self.ssl_context,
                            subprotocols=self.subprotocols,
                            extra_headers=self.extra_headers,
                            message_queue_size=self.message_queue_size,
                            max_message_size=self.max_message_size)
                    else:
                        self._connection = await connect_websocket(nursery, self.host, self.port,
                            self.resource, use_ssl=self.use_ssl, subprotocols=self.subprotocols,
                            extra_headers=self.extra_headers,
                            message_queue_size=self.message_queue_size,
                            max_message_size=self.max_message_size)
            except trio.TooSlowError:
                raise ConnectionTimeout from None
            except OSError as e:
                raise HandshakeError from e
            log.info('Slurry websocket connected.')
            if input is not None:
                if self.parse_json:
                    nursery.start_soon(send_json_task)
                else:
                    nursery.start_soon(send_task)
            try:
                while True:
                    message = await self._connection.get_message()
                    if self.parse_json:
                        await output(orjson.loads(message))
                    else:
                        await output(message)
            except ConnectionClosed:
                log.info('Slurry websocket read from closed connection.')
            except trio.BrokenResourceError:
                log.info('Slurry websocket write to closed pipeline.')
            finally:
                log.info('Slurry websocket stopping.')
                nursery.cancel_scope.cancel()
                try:
                    with trio.fail_after(self.disconnect_timeout):
                        await self._connection.aclose()
                except trio.TooSlowError:
                    raise DisconnectionTimeout from None
                finally:
                    log.info('Slurry websocket closed.')

    @property
    def closed(self) -> CloseReason:
        '''
        (Read-only) The reason why the connection was closed, or ``None`` if the
        connection is still open.

        .. note::
            The websocket is not actually initialized, until the enclosing pipeline is started.
            Before this time, the closed property will always return None.

        :rtype: CloseReason
        '''
        if self._connection is None:
            return None
        return self._connection.closed

    async def aclose(self, code=1000, reason=None):
        '''
        Close the WebSocket connection.
        '''
        if self._connection:
            return await self._connection.aclose(code, reason)
        raise ConnectionError('Websocket not started.')

    async def ping(self, payload=None):
        '''
        Send WebSocket ping to remote endpoint and wait for a correspoding pong.
        '''
        if self._connection:
            return await self._connection.ping(payload)
        raise ConnectionError('Websocket not started.')

    async def pong(self, payload=None):
        '''
        Send an unsolicted pong.
        '''
        if self._connection:
            return await self._connection.pong(payload)
        raise ConnectionError('Websocket not started.')

    async def send_message(self, message):
        '''
        Send a WebSocket message directly to the underlying websocket. (Normally, messages
        should be sent via the section input channel.)

        The corresponding ``WebSocketConnection``.``get_message`` call is not supported. Any
        returned messages are sent on the output channel.
        '''
        if self._connection:
            return await self._connection.send_message(message)
        raise ConnectionError('Websocket not started.')
