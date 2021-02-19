# external lib imports
import websockets
from urllib import parse

# internal lib imports
from .types import sendable, event_pair
from .PacketEncoder import AbstractPacketEncoder, DefaultPacketEncoder

# default lib imports
import ssl
import asyncio
import logging
from typing import Callable, Union
"""
NOT READY FOR USE, NOT TESTED, PLEASE IGNORE 
"""


# iot.io client implementation using Async
class AsyncIoTClient:
    def __init__(self, client_id: str, client_type: str, client_data: dict = None, logging_level: int = logging.WARNING,
                 encoder: AbstractPacketEncoder = DefaultPacketEncoder):
        # websocket object
        self.__socket = None

        # encoder used to encode and decode messages
        self.__encoder = encoder

        # if the client_data is not specified default to empty dictionary
        if client_data is None:
            client_data = {}

        # verify the client attributes are the correct types
        if not isinstance(client_id, str):
            raise ValueError("client_id must be a str.")
        if not isinstance(client_type, str):
            raise ValueError("client_type must be a str.")
        if not isinstance(client_data, dict):
            raise ValueError("client_data must be a dict.")

        # client attributes
        self.__id = client_id
        self.__type = client_type
        self.__data = client_data

        # logger instance
        self.logger = logging.getLogger("[iot.io.client]")
        self.logger.setLevel(logging_level)

        # event loop
        self.loop = asyncio.get_event_loop()

    # socket property
    @property
    def socket(self) -> websockets.WebSocketClientProtocol:
        return self.__socket

    # if the client is still connected
    @property
    def connected(self) -> bool:
        return not self.__socket.closed

    # main loop which receives messages
    async def handle(self):
        """
        Loop for receiving messages from the server and calling the given handler.

        :return:
        """

        # wait until the socket object is created
        while self.__socket is None:
            await asyncio.sleep(0)

        # wait until the socket is ready
        await self.__socket.ensure_open()

        # loop while socket is open
        while not self.__socket.closed:
            try:
                # wait to receive data from the socket
                data = await self.__socket.recv()

                # if data is None exit loop
                if data is None:
                    break

                # decode packet into event and message
                event, message = self.__encoder.decode(data)

                # check for parsing error
                if event is not None:
                    try:
                        # run the event's handler and get the event and message for the response
                        event, response = await self.__call_event_handler(event, message)

                        # if the response is not none send it
                        if response is not None:
                            await self.send(event, message)
                    except Exception as e:
                        self.logger.error("Exception when executing the handler for the '" + event
                                          + "' event. Error: " + str(e))
            except websockets.ConnectionClosedError as e:
                self.logger.error("Connection closed: " + str(e))
        self.logger.info("Disconnected.")

    # begins the client connection
    async def begin(self, domain: str, ssl_context: ssl.SSLContext = None, use_tls: bool = True):
        """
        Begins the client's connection to the server.

        :param domain: Domain or IP to connect to, like 'example.com', 'localhost:5000', or '192.168.1.10'.
        :param ssl_context: An SSL context for verifying a secure connection with the host.
        :param use_tls: If no ssl context is provided by the connection should still use TLS to encrypt communication.
                        Defaults to True for more secure communications!
        :return:
        """

        # create websocket object and connect to the server
        self.logger.info("Connecting to the domain: " + domain)

        # create the url
        url = domain + "/iot.io?" + parse.urlencode({
            "id": self.__id,
            "type": self.__type,
            "data": self.__data
        })

        if ssl_context is None:
            # if wss is specified then use it even without ssl_context
            if use_tls:
                self.__socket = await websockets.connect("wss://" + url)

            # if no ssl is provided use default
            self.__socket = await websockets.connect("ws://" + url)
        else:
            # use ssl if provided
            self.__socket = await websockets.connect("wss://" + url, ssl=ssl_context)

    # run the main loop with a blocking call
    def run(self, domain: str, ssl_context: ssl.SSLContext = None, use_tls: bool = True):
        """
        Start the client's connection while also preventing the program from closing. Runs the begin() function and
        then enters the main handling loop. (blocking)

        :param domain: Domain or IP to connect to, like 'example.com', 'localhost:5000', or '192.168.1.10'.
        :param ssl_context: An SSL context for verifying a secure connection with the host.
        :param use_tls: If no ssl context is provided by the connection should still use TLS to encrypt communication.
                        Defaults to True for more secure communications!
        :return:
        """
        self.loop.create_task(self.begin(domain, ssl_context, use_tls))
        self.loop.run_until_complete(self.handle())

    # will hand until the client is connected
    async def wait_until_ready(self):
        """
        Blocks the current thread when called until the client is ready.

        :return:
        """
        # wait until the socket object is created
        while self.__socket is None:
            await asyncio.sleep(0)

        # wait until the socket is open
        await self.__socket.ensure_open()

    # sends event message to the server
    async def send(self, event: str, message: sendable):
        """
        Send a message to the server for a given event.

        :param event: The event handler which the message will be delivered to.
        :param message: The message that will be passed to the event handler.
        :return: None
        """

        # typing
        self.__socket: websockets.WebSocketClientProtocol

        # check type of message
        if not isinstance(message, (bool, int, float, str, dict)):
            raise ValueError("A non-sendable value was passed to a client's send method.")

        # check if the connection is alive
        if not self.__socket.closed:
            # logging
            self.logger.debug("Sending a message for event '", event, "' with type: '", type(message), "'")

            # send the message
            await self.__socket.send(self.__encoder.encode(event, message))

    # wrapper for adding new handlers
    def on(self, event: str):
        """
        A decorator for defining event handlers without creating a subclass.

        :param event: The name of the event that will trigger the provided coroutine.
        :return:
        """

        # decorator function
        def decorator(coroutine: Callable[[sendable], Union[event_pair, None]]):
            # check if the coroutine is async, if it is not raise an error
            if not asyncio.iscoroutinefunction(coroutine):
                raise ValueError("Functions wrapped with the client.on decorator must be asynchronous.")

            # add the coroutine for the event
            setattr(self, "on_" + event, coroutine)

            # added function for event
            self.logger.debug("Added Handler: on_" + event)

        # return the decorator
        return decorator

    # calls the specific event handler if it exists
    async def __call_event_handler(self, event: str, message: str) -> event_pair:
        """
        Calls the event handler for the given event if it exists, if it doesnt exist then it does nothing.

        Don't overwrite.

        :param event: The event which is being invoked.
        :param message: The message to pass to the event handler.
        :return: None or str
        """
        try:
            # void "connect" and "disconnect" events
            if event == "connect" or event == "disconnect":
                return None, None

            self.logger.debug("Calling Event Handler: on_" + event)

            # call the handler and check for a response
            response = await getattr(self, "on_" + event)(message)

            if response is None:
                return None, None
            else:
                return event, response
        except AttributeError:
            return None, None
