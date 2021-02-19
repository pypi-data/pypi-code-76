# external lib imports
import websocket
import json

# internal lib imports
from .types import sendable, event_pair
from .PacketEncoder import AbstractPacketEncoder, DefaultPacketEncoder
from .Endpoint import EndpointInfo
from .Errors import Errors
from .__main__ import __protocol_version__


# default lib imports
import ssl
import time
import logging
from typing import Callable, Union


# iot.io client implementation
class IoTClient:
    def __init__(self, client_id: str, client_type: str, client_data: dict = None, logging_level: int = logging.WARNING,
                 encoder: AbstractPacketEncoder = DefaultPacketEncoder):
        # socket object
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

        # fatal exception flag (keeps track of if the server has notified the client of a fatal exception)
        self.__fatal_exception = False

        # a list of endpoint information which will be passed to the server when establishing a connection
        self.__endpoint_info = []

        # logger instance
        self.logger = logging.getLogger("[iot.io.client]")
        self.logger.setLevel(logging_level)

    # blocks until the client connection is open
    def ensure_open(self):
        """
        Blocking call which will unblock once the client connection has been created and connected.

        :return:
        """
        # wait for socket to be created
        while self.__socket is None:
            pass

        # wait for socket to be connected
        while not self.__socket.connected:
            pass

    # if the client is connected
    @property
    def connected(self) -> bool:
        """
        Returns true if the client has connected to the server, false otherwise.

        :return: bool
        """
        # return false if the socket does not exist
        if self.__socket is None:
            return False

        # return false if the fatal exception flag was triggered
        if self.__fatal_exception:
            return False

        return self.__socket.connected

    # handler
    def handle(self):
        """
        Blocking call which handles the client receiving data for the lifetime of the socket connection.

        :return: None
        """
        # wait until the client is connected
        self.ensure_open()

        # loop while socket is open
        while self.__socket.connected:

            try:
                # wait for data
                data = self.__socket.recv()
            except ConnectionAbortedError as e:
                self.logger.error("Exception when calling socket.recv(): ", str(e))
                break
            except websocket.WebSocketProtocolException:
                self.logger.error("Server specified did not allow for a connection.")
                break

            # ignore plain string data
            if isinstance(data, str):
                continue

            try:
                # decode packet into event and message
                event, message = self.__encoder.decode(data)
            except Exception as e:
                self.logger.error("Exception when decoding message: ", e)
                continue

            try:
                # run the event's handler and get the event and message for the response
                event, response = self.__call_event_handler(event, message)

                # if the response is not none send it
                if response is not None:
                    self.send(event, message)
            except Exception as e:
                self.logger.error("Exception when executing the handler for the '" + event
                                  + "' event. Error: " + str(e))

        try:
            # call disconnect handler
            self.__call_event_handler("disconnect", "")
        except Exception as e:
            self.logger.error("Exception when executing the handler for the 'on_disconnect' event. Error: " + str(e))

        # log disconnected
        self.logger.info("Disconnected.")

    def connect(self, domain: str, timeout: int = None, sslopt: dict = None, use_tls: bool = True):
        """
        Begins the client's connection to the server.

        :param timeout: Timeout before connection is aborted.
        :param domain: Domain or IP to connect to, like 'example.com', 'localhost:5000', or '192.168.1.10'.
        :param sslopt: SSL Options used by the websocket-client library.
        :param use_tls: If no ssl context is provided by the connection should still use TLS to encrypt communication.
                        Defaults to True for more secure communications!
        :return: None
        """

        # create websocket object and connect to the server
        self.logger.info("Connecting to the domain: " + domain)

        # create the url
        url = domain + "/iot.io"

        # create headers
        request_headers = {
            "IoT-IO-Id": self.__id,
            "IoT-IO-Type": self.__type,
            "IoT-IO-Data": json.dumps(self.__data),
            "IoT-IO-Endpoints": json.dumps(self.__endpoint_info),
            "IoT-IO-ProtocolVersion": __protocol_version__
        }

        if sslopt is None:
            # if wss is specified then use it even without ssl_context
            if use_tls:
                self.__socket = websocket.create_connection("wss://" + url, timeout=timeout, header=request_headers)

            # if no ssl is provided use default
            self.__socket = websocket.create_connection("ws://" + url, timeout=timeout, header=request_headers, sslopt={
                "check_hostname": False,
                "cert_reqs": ssl.CERT_NONE
            })
        else:
            # use ssl if provided
            self.__socket = websocket.create_connection("wss://" + url, timeout=timeout, header=request_headers,
                                                        sslopt=sslopt)

        try:
            # call connect handler
            self.__call_event_handler("connect", "")
        except Exception as e:
            self.logger.error("Exception when executing the handler for the 'on_connect' event. Error: " + str(e))

        # log connected
        self.logger.info("Connected successfully.")

    # run function which connects and handles the connection in a single blocking call
    def run(self, domain: str, timeout: int = None, sslopt: dict = None, use_tls: bool = True, reconnect: bool = True,
            reconnect_delay: int = 15):
        """
        Run function which connects and handles the connection in a single blocking call. If reconnect is enabled
        then the timeout error from connect is suppressed and the connection is attempted again.

        :param timeout: Timeout before connection is aborted.
        :param domain: Domain or IP to connect to, like 'example.com', 'localhost:5000', or '192.168.1.10'.
        :param sslopt: SSL Options used by the websocket-client library.
        :param use_tls: If no ssl context is provided by the connection should still use TLS to encrypt communication.
                        Defaults to True for more secure communications!
        :param reconnect: If the client should reconnect. True for reconnection, false for exit on connection end.
        :param reconnect_delay: Delay between re-connections.
        :return: None
        """
        # main run loop
        while True:
            # if a fatal exception was signaled end the loop
            if self.__fatal_exception:
                # close the client connection
                self.__socket.close()

                self.logger.error("A fatal exception was triggered by the server, stopping reconnection loop.")
                break

            # catch timeout errors
            try:
                # connect to the server
                self.connect(domain, timeout, sslopt, use_tls)

                # handle connection once connected
                self.handle()
            except TimeoutError:
                self.logger.error("Client Connection failed due to timeout.")
                continue
            except ConnectionRefusedError:
                self.logger.error("Connection refused by host.")
                continue
            except ConnectionResetError:
                try:
                    # call disconnect handler
                    self.__call_event_handler("disconnect", "")
                except Exception as e:
                    self.logger.error(
                        "Exception when executing the handler for the 'on_disconnect' event. Error: " + str(e))

                # log disconnected
                self.logger.info("Disconnected.")
            finally:
                # if reconnect is not true break
                if not reconnect:
                    break
                else:
                    # log and wait for the reconnect delay
                    self.logger.info("Waiting " + str(reconnect_delay) + " seconds before attempting to re-connect.")
                    time.sleep(reconnect_delay)

    # sends event message to the server
    def send(self, event: str, message: sendable):
        """
        Send a message to the server for a given event.

        :param event: The event handler which the message will be delivered to.
        :param message: The message that will be passed to the event handler.
        :return: None
        """
        # check type of message
        if not isinstance(message, (bytes, bytearray, bool, int, str, list, dict)):
            raise ValueError("A non-sendable value was passed to a client's send method.")

        # check if the connection is alive
        if self.__socket.connected:
            # logging
            self.logger.debug("Sending a message for event '" + event + "' with type: '" + str(type(message)) + "'")

            # send the message
            self.__socket.send(self.__encoder.encode(event, message), websocket.ABNF.OPCODE_BINARY)

    # wrapper for adding new handlers
    def on(self, event: str, endpoint_info: EndpointInfo = None):
        """
        A decorator for defining event handlers without creating a subclass.

        :param event: The name of the event that will trigger the provided coroutine.
        :param endpoint_info: A EndpointConstraint object which defines the type of data this endpoint will
        accept. Is passed to the sever and can be used to auto-generate a server REST API endpoint for this handler. If
        no EndpointConstraint is provided then the server will be in the dark about the type of data this endpoint
        can accept.
        :return:
        """
        # decorator function
        def decorator(handler: Callable[[sendable], Union[event_pair, None]]):
            # add the handler for the event
            setattr(self, "on_" + event, handler)

            if endpoint_info:
                # add the constraint
                self.__endpoint_info.append(endpoint_info.get_info(event))

            # added function for event
            self.logger.debug("Added Handler: on_" + event)

        # return the decorator
        return decorator

    # calls the specific event handler if it exists
    def __call_event_handler(self, event: str, message: sendable) -> event_pair:
        """
        Calls the event handler for the given event if it exists, if it doesnt exist then it does nothing.

        Don't overwrite.

        :param event: The event which is being invoked.
        :param message: The message to pass to the event handler.
        :return: None or str
        """
        try:
            response = None

            # call "connect" and "disconnect"
            if event == "connect":
                self.on_connect()
            elif event == "disconnect":
                self.on_disconnect()
            elif event == "error":
                # call builtin error handler
                self.__on_error(message)

                # call overrideable on_error function
                self.on_error(message)
            else:
                self.logger.debug("Calling Event Handler: on_" + event)

                # call the handler and check for a response
                response = getattr(self, "on_" + event)(message)

            if isinstance(response, tuple):
                event = response[0]
                response = response[1]

            if response is None:
                return None, None
            else:
                return event, response
        except AttributeError:
            return None, None

    # builtin error handler
    def __on_error(self, error: str):
        # get the Error enum from the error string
        error = Errors.get(error, None)

        if error == Errors.CLIENT_NO_ID:
            self.logger.error("Connection Rejected Error: Client failed to provide the IoT-IO-Id header field.")
            self.__fatal_exception = True
        elif error == Errors.CLIENT_NO_TYPE:
            self.logger.error("Connection Rejected Error: Client failed to provide the IoT-IO-Type header field.")
            self.__fatal_exception = True
        elif error == Errors.CLIENT_INVALID_TYPE:
            self.logger.error("Connection Rejected Error: Client provided an invalid value for the IoT-IO-Type "
                              "header field.")
            self.__fatal_exception = True
        elif error == Errors.CLIENT_INVALID_DATA:
            self.logger.error("Connection Rejected Error: Client provided an invalid json data for the IoT-IO-Data "
                              "header field.")
            self.__fatal_exception = True
        elif error == Errors.CLIENT_INVALID_DATA:
            self.logger.error("Connection Rejected Error: Client provided an invalid json data for the IoT-IO-Data "
                              "header field.")
            self.__fatal_exception = True
        elif error == Errors.CLIENT_INVALID_ENDPOINTS:
            self.logger.error("Connection Rejected Error: Client provided an invalid value for the IoT-IO-Endpoints "
                              "header field.")
            self.__fatal_exception = True
        elif error == Errors.CLIENT_NO_PROTOCOL_VERSION:
            self.logger.error("Connection Rejected Error: Client did not provide the IoT-IO-ProtocolVersion "
                              "header field.")
            self.__fatal_exception = True
        elif error == Errors.CLIENT_INCOMPATIBLE_PROTOCOL_VERSION:
            self.logger.error("Connection Rejected Error: The version of the client's protocol is incompatible "
                              "with that of the server.")
            self.__fatal_exception = True
        elif error == Errors.CLIENT_INVALID_PACKET:
            self.logger.error("Communication Error: Unable to decode sent packet.")
        else:
            self.logger.error("Unknown Error: " + str(error))

    # default error handler
    def on_error(self, error: str):
        pass

    # basic on_connect and on_disconnect handlers
    def on_connect(self) -> Union[None, event_pair]:
        pass

    def on_disconnect(self):
        pass


