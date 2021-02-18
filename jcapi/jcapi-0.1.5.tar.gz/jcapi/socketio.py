"""Small SocketIO client via Websockets."""
import collections
import json
import logging
import threading

from datetime import datetime
from random import random

from lomonds import WebSocket
from lomonds import events
from lomonds.persist import persist
from lomonds.errors import WebSocketError

from .error_handling import SocketIOException

STARTED = "started"
STOPPED = "stopped"
CONNECTED = "connected"
DISCONNECTED = "disconnected"
DEVICE_UPDATE_EVENT = "device_updated"
PING = "ping"
PONG = "pong"
POLL = "poll"
EVENT = "event"
ERROR = "error"

PING_INTERVAL = "pingInterval"
PING_TIMEOUT = "pingTimeout"

COOKIE_HEADER = str.encode("Cookie")
ORIGIN_HEADER = str.encode("Origin")

# URL_PARAMS = "?EIO=3&transport=websocket"

_LOGGER = logging.getLogger(__name__)


class SocketIO():
    """Class for using websockets to talk to a SocketIO server."""

    def __init__(self, url, cookie=None, token=None, origin=None):
        """Init SocketIO class."""
        self._url = url
        if origin:
            self._origin = origin.encode()
        else:
            self._origin = None

        if cookie:
            self._cookie = cookie.encode()
        else:
            self._cookie = None

        self._thread = None
        self._websocket = None
        self._exit_event = None
        self._running = False

        self._websocket_connected = False
        self._engineio_connected = False
        self._socketio_connected = False

        self._ping_interval_ms = 80000
        self._ping_timeout_ms = 60000
        self.token = token

        self._last_ping_time = datetime.min
        self._last_packet_time = datetime.min

        self._callbacks = collections.defaultdict(list)

    def set_origin(self, origin=None):
        """Set the Origin header."""
        if origin:
            self._origin = origin.encode()
        else:
            self._origin = None

    def set_cookie(self, cookie=None):
        """Set the Cookie header."""
        if cookie:
            self._cookie = cookie.encode()
        else:
            self._cookie = None

    # pylint: disable=C0103
    def on(self, event_name, callback):
        """Register callback for a SocketIO event."""
        if not event_name:
            return False

        _LOGGER.debug("Adding callback for event name: %s", event_name)

        self._callbacks[event_name].append((callback))

        return True

    def start(self):
        """Start a thread to handle SocketIO notifications."""
        if not self._thread:
            _LOGGER.info("Starting SocketIO thread...")

            self._thread = threading.Thread(target=self._run_socketio_thread,
                                            name='SocketIOThread')
            self._thread.deamon = True
            self._thread.start()

    def stop(self):
        """Tell the SocketIO thread to terminate."""
        if self._thread:
            _LOGGER.info("Stopping SocketIO thread...")

            # pylint: disable=W0212
            self._running = False

            if self._exit_event:
                self._exit_event.set()

            self._thread.join()

    def _run_socketio_thread(self):
        self._running = True

        # Back off for Error restarting
        min_wait = 5
        max_wait = 30

        retries = 0

        random_wait = max_wait - min_wait

        while self._running is True:
            _LOGGER.info(
                "Attempting to connect to SocketIO server...")

            try:
                retries += 1

                self._handle_event(STARTED, None)

                self._websocket = WebSocket(self._url)
                self._exit_event = threading.Event()

                if self._cookie:
                    self._websocket.add_header(COOKIE_HEADER, self._cookie)

                if self._origin:
                    self._websocket.add_header(ORIGIN_HEADER, self._origin)

                for event in persist(self._websocket, ping_rate=8, ping_data=b'status:state',
                                     exit_event=self._exit_event):
                    if isinstance(event, events.Connected):
                        retries = 0
                        self._on_websocket_connected(event)
                    elif isinstance(event, events.Disconnected):
                        self._on_websocket_disconnected(event)
                    elif isinstance(event, events.Text):

                        self._on_websocket_text(event)
                    elif isinstance(event, events.Poll):
                        self._on_websocket_poll(event)
                    elif isinstance(event, events.BackOff):
                        self._on_websocket_backoff(event)

                    if self._running is False:
                        self._websocket.close()

            except SocketIOException as exc:
                _LOGGER.warning("SocketIO Error: %s", exc.details)

            except WebSocketError as exc:
                _LOGGER.warning("Websocket Error: %s", exc)

            if self._running:
                wait_for = min_wait + random() * min(random_wait, 2 ** retries)

                _LOGGER.info("Waiting %f seconds before reconnecting...",
                             wait_for)

                if self._exit_event.wait(wait_for):
                    break

        self._handle_event(STOPPED, None)

    def _on_websocket_connected(self, _event):
        self._websocket_connected = True
        self._websocket.send_text(f"token:{self.token}")

        _LOGGER.info("Websocket Connected")

        self._handle_event(CONNECTED, None)

    def _on_websocket_disconnected(self, _event):
        self._websocket_connected = False
        self._engineio_connected = False
        self._socketio_connected = False

        _LOGGER.info("Websocket Disconnected")

        self._handle_event(DISCONNECTED, None)

    def _on_websocket_poll(self, _event):
        last_packet_delta = datetime.now() - self._last_packet_time
        last_packet_ms = int(last_packet_delta.total_seconds() * 1000)

        if self._engineio_connected and last_packet_ms > self._ping_timeout_ms:
            _LOGGER.warning("SocketIO Server Ping Timeout")
            self._websocket.close()
            return

        last_ping_delta = datetime.now() - self._last_ping_time
        last_ping_ms = int(last_ping_delta.total_seconds() * 1000)

        if self._engineio_connected and last_ping_ms >= self._ping_interval_ms:
            self._last_ping_time = datetime.now()
            _LOGGER.debug("Client Ping")
            self._handle_event(PING, None)

        self._handle_event(POLL, None)

    def _on_websocket_text(self, _event):
        self._last_packet_time = datetime.now()
        if "getDevListJson-page" in _event.text:
            s = json.loads(_event.text).get("value", None)
            self._handle_event(DEVICE_UPDATE_EVENT, s)

        _LOGGER.debug("Ignoring EngineIO packet: %s", _event.text)

    # pylint: disable=R0201
    def _on_websocket_backoff(self, _event):
        return

    def _on_engineio_opened(self, _packet_data):
        json_data = json.loads(_packet_data)

        if json_data and json_data[PING_INTERVAL]:
            ping_interval_ms = json_data[PING_INTERVAL]
            _LOGGER.debug("Set ping interval to: %d", ping_interval_ms)

        if json_data and json_data[PING_TIMEOUT]:
            ping_timeout_ms = json_data[PING_TIMEOUT]
            _LOGGER.debug("Set ping timeout to: %d", ping_timeout_ms)

        self._engineio_connected = True

        _LOGGER.debug("EngineIO Connected")

    def _on_engineio_closed(self):
        self._engineio_connected = False

        _LOGGER.debug("EngineIO Disconnected")

        self._websocket.close()

    def _on_engineio_pong(self):
        _LOGGER.debug("Server Pong")
        self._handle_event(PONG, None)

    def _on_socketio_connected(self):
        self._socketio_connected = True

        _LOGGER.debug("SocketIO Connected")

    def _on_socketio_disconnected(self):
        self._socketio_connected = False

        _LOGGER.debug("SocketIO Disconnected")

        self._websocket.close()

    def _on_socketio_error(self, _message_data):
        self._handle_event(ERROR, _message_data)

    def _handle_event(self, event_name, event_data):
        for callback in self._callbacks.get(event_name, ()):
            try:
                if event_data:
                    callback(event_data)
                else:
                    callback()
            # pylint: disable=W0703
            except Exception as exc:
                _LOGGER.exception(
                    "Captured exception during SocketIO event callback: %s",
                    exc)
