import asyncio
import websockets
import ssl
import re
import json
import logging
from typing import Union, Tuple

# define the sendable type (Union of types which can be sent to clients)
sendable = Union[int, bool, float, str, dict]

# define the event_pair type
event_pair = Union[Tuple[None, None], Tuple[str, sendable]]


# iot.io client implementation
class IoTClient:
    def __init__(self, client_id: str, client_type: str, client_data: dict, logging_level: int = logging.WARNING):
        # websocket object
        self.socket = None

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

        # keeps track of if the handshake packet has been sent
        self.handshake_sent = False

        # logger instance
        self.logger = logging.getLogger("[iot.io.client]")
        self.logger.setLevel(logging_level)

        # event loop
        self.loop = asyncio.get_event_loop()

    # main loop which receives messages
    async def handle(self):
        """
        Loop for receiving messages from the server and calling the given handler.

        :return:
        """

        # wait until the socket object is created
        while self.socket is None:
            await asyncio.sleep(0)

        # wait until the socket is ready
        await self.socket.ensure_open()

        # send the handshake packet
        await self._handshake()
        self.logger.info("Connected.")

        while not self.socket.closed:
            # wait to receive data from the socket
            try:
                message = await self.socket.recv()

                # exit if message is None
                if message is None:
                    break

                # parse the message
                event, message = self.parse_message(message)

                # check if it was parsed correctly
                if event is not None:
                    try:
                        # run the correct handler
                        await self.__call_event_handler(event, message)
                    except Exception as e:
                        self.logger.error("Exception when executing the handler for the '" + event
                                          + "' event. Error: " + str(e))
            except websockets.ConnectionClosedError as e:
                self.logger.error("Connection closed: " + str(e))
        self.logger.info("Disconnected.")

    # begins the client connection
    async def begin(self, domain: str, ssl_context: ssl.SSLContext = None):
        """
        Begins the client's connection to the server.

        :param domain:
        :param ssl_context:
        :return:
        """

        # create websocket object and connect to the server
        self.logger.info("Connecting to the domain: " + domain)

        if ssl_context is None:
            # if no ssl is provided use default
            self.socket = await websockets.connect("ws://" + domain + "/iot.io")
        else:
            # use ssl if provided
            self.socket = await websockets.connect("wss://" + domain + "/iot.io", ssl=ssl_context)

    # run the main loop with a blocking call
    def run(self, domain: str, ssl_context: ssl.SSLContext = None):
        """
        Start the client's connection while also preventing the program from closing.

        :return:
        """
        self.loop.create_task(self.begin(domain, ssl_context))
        self.loop.run_until_complete(self.handle())

    # will hand until the client is connected
    async def wait_until_ready(self):
        """
        Blocks the current thread when called until the client is ready.

        :return:
        """
        # wait until the socket object is created
        while self.socket is None:
            await asyncio.sleep(0)

        # wait until the socket is open
        await self.socket.ensure_open()

        # wait until the handshake packet has been sent
        while not self.handshake_sent:
            await asyncio.sleep(0)

    # takes in a list of args (must be str) and forms a a iot.io packet
    @staticmethod
    def _create_packet(*args: str) -> str:
        """
        Create a iot.io packet given args which are all strings.

        :param args:
        :return: Configured iot.io packet as a str.
        """
        # final packet
        packet = ""

        # add each arg to the packet
        for arg in args:
            # ensure str only
            if not isinstance(arg, str):
                raise ValueError("All arguments must be a str.")

            # add the arg to the packet
            packet += "[/\"" + arg + "\"/]"

        # return the finished packet
        return packet

    # send the server the handshake packet
    async def _handshake(self):
        """
        Sends a handshake packet to  the server so the server knows this client's id, type, and data.

        :return: None
        """

        # send the handshake packet
        self.logger.debug("Sending handshake message.")
        await self.socket.send(self._create_packet(self.__id, self.__type, json.dumps(self.__data)))

        # TODO add handshake confirmation

        # set the handshake_sent flag to true
        self.handshake_sent = True

    # sends event message to the server
    async def send(self, event: str, message: sendable):
        """
        Send a message to the server for a given event.

        :param event: The event handler which the message will be delivered to.
        :param message: The message that will be passed to the event handler.
        :return: None
        """

        self.socket: websockets.WebSocketClientProtocol

        # check type of message
        if not isinstance(message, (bool, int, float, str, dict)):
            raise ValueError("A non-sendable value was passed to a client's send method.")

        # conversions from sendable to string
        if isinstance(message, dict):
            # serialize the dict as a json string
            message = json.dumps(message)
        # convert generics to string counterpart
        else:
            # convert to string
            message = str(message)

        # check if the connection is alive
        if not self.socket.closed:
            # logging
            self.logger.debug("Sending a message for event '" + event + "': " + message)

            # send the message
            await self.socket.send(self._create_packet(event, message))

    # wrapper for adding new handlers
    def on(self, event: str):
        """
        A decorator for defining event handlers without creating a subclass.

        :param event: The name of the event that will trigger the provided coroutine.
        :return:
        """
        # decorator function
        def decorator(coroutine):
            # check if the coroutine is async, if it is not raise an error
            if not asyncio.iscoroutinefunction(coroutine):
                raise ValueError("Functions wrapped with the client.on decorator must be asynchronous.")

            # add the coroutine for the event
            setattr(self, "on_" + event, coroutine)

        # return the decorator
        return decorator

    # parse a iot.io packet and return the contents as a list
    @staticmethod
    def parse(message: str) -> list:
        """
        Messages between the client and server are formatted as a list, which each
         element being an argument. For example the handshake packet the client first sends to the server
         is structured like the following list: (id, type, data).

         This same packet would be sent as the following string by the client:
            '[/"1"/][/"id"/][/"type"/][/"data"/]'

        This parser takes than string and converts it to the following list:
            ['1', 'id', 'type', 'data']

        :param message: the message to be parsed as a string
        :return: a list of parsed arguments
        """

        # parse the message to return contents
        result = re.findall("\[/\"([^[\]]*)\"/\]", message)

        return result

    # parse a normal message packet
    def parse_message(self, packet: str) -> event_pair:
        """
        Parse what is expected to be a basic iot.io message, returning the event and message

        :param packet: The iot.io packet to parse.
        :return: A event pair. [(None, None) or (str, sendable)]
        """
        # parse the packet
        args = self.parse(packet)

        # check for correct length
        if len(args) != 2:
            self.logger.warning("When attempting to parse a message a invalid message format was received. ("
                                "Raw Message: " + str(packet) + " | Parsed Message: " + str(args) + ")")
            return None, None

        # attempt deserialization of message
        try:
            args[1] = json.loads(args[1])
        except ValueError or json.JSONDecodeError:
            pass

        # return the event and the message
        return args[0], args[1]

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

            # call the handler and check for a response
            response = await getattr(self, "on_" + event)(message)

            if response is None:
                return None, None
            else:
                return event, response
        except AttributeError:
            return None, None
