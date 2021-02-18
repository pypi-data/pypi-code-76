# default lib imports
import logging
from eventlet import websocket
from eventlet.websocket import WebSocket
from typing import List, Dict

# external lib imports
from flask import Flask

# lib imports
from .IoTClient import IoTClient
from .DeviceType import DeviceType
from .error import ConnectionEnded
from .types import event_pair, sendable


class IoTManagerMiddleware(object):
    def __init__(self, app, wsgi_app, manager: 'IoTManager'):
        self.app = app
        self.wsgi_app = wsgi_app
        self.manager = manager

        # eventlet websocket server handler
        @websocket.WebSocketWSGI
        def ws(socket: WebSocket):
            # pass the socket of to the manager
            manager.socket(socket)

        # save the generator
        self.ws = ws

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"] == "/iot.io":
            self.ws(environ, start_response)

            return []

        return self.wsgi_app(environ, start_response)


# main class used for implimentation
class IoTManager(object):
    """
    Main library instance.
    """

    def __init__(self, app: Flask, logging_level: int = logging.ERROR, client_logging_level: int = logging.ERROR):
        # reference to flask app
        self.app = app

        if app:
            self.init_app(app)

        # list of active clients
        self.__clients: List[IoTClient]
        self.__clients = []

        # a dict of device types
        self.__types: Dict[str, DeviceType]
        self.__types = {}

        # dict which is used for storing room information
        self.__rooms = {}

        # logger for the manager
        self.logger = logging.Logger("[iot.io.server]")

        # logging levels for main and client debuggers
        self.logger.setLevel(logging_level)
        self.client_logging_level = client_logging_level

    # function for adding middleware
    def init_app(self, app: Flask):
        app.wsgi_app = IoTManagerMiddleware(app, app.wsgi_app, self)

    # function for handling new websocket clients
    def socket(self, ws: WebSocket):
        # create a new client
        try:
            # create a new client object if the client sends the handshake packet successfully
            client = IoTClient(ws, self.client_logging_level)
        except ConnectionEnded:
            # exit if the handshake fails
            return

        # check if the client has a valid type
        if self.__types.get(client.type, None) is None:
            # log and exit if the client has an invalid type
            self.logger.warning("Client with ID '" + client.id + "' claimed a device type of '" + client.type
                                + "' but no such device type was defined. Refusing connection.")
            return

        # remove a client with the same id if it exists (getting rid of ghost clients)
        self.remove_client_by_id(client.id)

        # add the client to the client list
        self.__clients.append(client)

        # call the on_connect handler
        self.__on_connect_handlers(client)

        # begin the loop of accepting messages for the client
        client.loop(self.__handle_event_message)

        # remove the client
        self.remove_client(client)

    # remove a client
    def remove_client(self, client: IoTClient):
        if client is None:
            return

        # call the on_disconnect handler
        self.__on_disconnect_handlers(client)

        # remove the client from the rooms
        for room in self.__rooms.keys():
            # remove the client from the room
            self.__rooms[room] = [x for x in self.__rooms[room] if x.id != client.id]

        # remove the client from the list of clients
        self.__clients = [x for x in self.__clients if client.id != x.id]

    # remove a client given it's id
    def remove_client_by_id(self, client_id: str):
        for client in self.__clients:
            if client.id == client_id:
                self.remove_client(client)

    # property which lists the IDs of all currently connected clients
    @property
    def connected_clients(self):
        return [x.id for x in self.__clients]

    # handles the device specific and generic on_connect handlers for the specified client
    def __on_connect_handlers(self, client: IoTClient):
        """
        Execute the generic and device specific on_connect handler.

        :param client: New client object.
        :return:
        """

        try:
            # call the type specific handler
            self.__types[client.type].on_connect(client)
        except Exception as e:
            # log the exception
            self.logger.error("Error when calling the type specific on_connect handler for client '" + client.id
                              + "': " + str(e))

        try:
            # call the generic handler
            self.on_connect(client)
        except Exception as e:
            # log the exception
            self.logger.error("Error when calling generic on_connect handler for client '" + client.id
                              + "': " + str(e))

    # handles the device specific and generic on_disconnect handlers for the specified client
    def __on_disconnect_handlers(self, client: IoTClient):
        """
        Execute the generic and device specific on_disconnect handler.

        :param client: New client object.
        :return:
        """

        try:
            # call the type specific handler
            self.__types[client.type].on_disconnect(client)
        except Exception as e:
            # log the exception
            self.logger.error("Error when calling the type specific on_disconnect handler for client '" + client.id
                              + "': " + str(e))

        try:
            # call the generic handler
            self.on_disconnect(client)
        except Exception as e:
            # log the exception
            self.logger.error("Error when calling generic on_disconnect handler for client '" + client.id
                              + "': " + str(e))

    # callback for when a client receives a message, sends it to the proper handler and squashes errors
    def __handle_event_message(self, event: str, message: str, client: IoTClient) -> event_pair:
        """
        Handles a given event and message given the client by executing the call_event_handler of the client's type.

        :param event: The event handler to trigger.
        :param message: The message to pass to the handler.
        :param client: The client object to pass to the handler.
        :return:
        """

        # activate the client type's event handler
        return self.__types[client.type].call_event_handler(event, message, client)

    # used to add a new device type to the manager
    def add_type(self, device: DeviceType):
        """
        Define a new device type for the Manager.

        :param device: Any implementation of the subclass DeviceType.
        :return: None
        """

        # ensure the device is of type DeviceType
        if not isinstance(device, DeviceType):
            raise ValueError("device is not of type DeviceType")

        # ensure device.type is of type str
        if not isinstance(device.type, str):
            raise ValueError("device.type is not of type str")

        # give the device object context of the manager
        device.set_context(self)

        # add the device to the list of device types
        self.__types.update({device.type: device})

        # logging output
        self.logger.debug("Successfully added DeviceType '" + device.type + "'.")

    # send a message to client(s)
    def emit(self, event: str, message: sendable, client_id: str = None, client_type: str = None, room: str = None):
        # if a client_id is provided
        if client_id is not None:
            # find the client with the provided id
            for client in self.__clients:
                if client.id == client_id:
                    # send the message
                    return client.send(event, message)
        elif client_type is not None:
            # send messages to the clients of given types
            for client in self.__clients:
                if client.type == client_type:
                    # send the message
                    client.send(event, message)
        elif room is not None:
            # check if the room exists
            if self.__rooms.get(room, None) is not None:
                for client in self.__rooms[room]:
                    # send the message
                    client.send(event, message)
        else:
            #
            raise ValueError("'client_id', 'client_type', or 'room' must be provided")

    # add a client to a room
    def join(self, client: IoTClient, room: str):
        # ensure types
        if not isinstance(client, IoTClient):
            raise ValueError("'client' must be an instance of a IoTClient")
        elif not isinstance(room, str):
            raise ValueError("'room' must be an instance of str")

        # check if the room exists yet
        if self.__rooms.get(room, None) is None:
            # create a new room entry with the client
            self.__rooms[room] = [client]
        else:
            # add the client to an existing room
            self.__rooms[room].append(client)

    # remove a client from a room
    def leave(self, client: IoTClient, room: str):
        # ensure types
        if not isinstance(client, IoTClient):
            raise ValueError("'client' must be an instance of a IoTClient")
        elif not isinstance(room, str):
            raise ValueError("'room' must be an instance of str")

        # check if the room exists
        if self.__rooms.get(room, None) is None:
            # exit since the room does not exist
            return
        else:
            # remove the client from the room if it is there
            self.__rooms[room] = [x for x in self.__rooms[room] if x.id != client.id]

    # event decorator function
    def event(self, coroutine):
        """
        Decorator which allows for simple overwriting of the generic on_connect, and
        on_disconnect functions.

        :param coroutine: Function named on_connect, or on_disconnect.
        :return: bool
        """

        # handle general on_connect, and on_disconnect handlers
        if coroutine.__name__ == "on_connect" or coroutine.__name__ == "on_disconnect":
            # logging output
            self.logger.info("Event handler '" + coroutine.__name__ + "' was added successfully.")

            # replaces the existing coroutine with the provided one
            setattr(self, coroutine.__name__, coroutine)
            return True
        return False

    def on_connect(self, client: IoTClient):
        """
        A empty implementation of the generic on_connect function, meant to be overwritten.

        Runs when any device connects to the server.

        :param client: Client object representing the connecting client.
        :return: None or str.
        """
        pass

    def on_disconnect(self, client: IoTClient):
        """
        A empty implementation of the generic on_disconnect function, meant to be overwritten.

        Runs when any device disconnects from the server.

        :param client: Client object representing the disconnecting client.
        :return: None.
        """
        pass
