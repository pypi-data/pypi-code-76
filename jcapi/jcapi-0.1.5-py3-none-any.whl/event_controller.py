"""Abode cloud push events."""
import collections
import logging

import jcapi.socketio as sio
import collections

_LOGGER = logging.getLogger(__name__)


class JcEventController():
    """Class for subscribing to abode events."""

    def __init__(self, JcAccount, url, token=None):
        """Init event subscription class."""
        self._jc_account = JcAccount
        self._thread = None
        self._running = False
        self._connected = False

        # Setup callback dicts
        self._connection_status_callbacks = collections.defaultdict(list)
        self._device_callbacks = collections.defaultdict(list)

        # Setup SocketIO
        self._socketio = sio.SocketIO(url=f"ws://{url}", token=token)

        # Setup SocketIO Callbacks
        self._socketio.on(sio.STARTED, self._on_socket_started)
        self._socketio.on(sio.CONNECTED, self._on_socket_connected)
        self._socketio.on(sio.DISCONNECTED, self._on_socket_disconnected)
        self._socketio.on(sio.DEVICE_UPDATE_EVENT, self._on_device_update)

    def start(self):
        """Start a thread to handle Abode SocketIO notifications."""
        self._socketio.start()

    def stop(self):
        """Tell the subscription thread to terminate - will block."""
        self._socketio.stop()

    def add_connection_status_callback(self, unique_id, callback):
        """Register callback for Abode server connection status."""
        if not unique_id:
            return False

        _LOGGER.debug(
            "Subscribing to Abode connection updates for: %s", unique_id)

        self._connection_status_callbacks[unique_id].append((callback))

        return True

    def remove_connection_status_callback(self, unique_id):
        """Unregister connection status callbacks."""
        if not unique_id:
            return False

        _LOGGER.debug(
            "Unsubscribing from Abode connection updates for : %s", unique_id)

        self._connection_status_callbacks[unique_id].clear()

        return True

    @property
    def connected(self):
        """Get the Abode connection status."""
        return self._connected

    @property
    def socketio(self):
        """Get the SocketIO instance."""
        return self._socketio

    def _on_socket_started(self):
        """Socket IO startup callback."""
        # pylint: disable=W0212
        pass

    def _on_socket_connected(self):
        """Socket IO connected callback."""
        self._connected = True

    def _on_socket_disconnected(self):
        """Socket IO disconnected callback."""
        self._connected = False

        for callbacks in self._connection_status_callbacks.items():
            # Check if list is not empty.
            # Applicable when remove_all_device_callbacks
            # is called before _on_socket_disconnected.
            if callbacks[1]:
                for callback in callbacks[1]:
                    _execute_callback(callback)

    def _on_device_update(self, data):
        """Device callback from Abode SocketIO server."""
        # print("receive update, processsing")
        self._jc_account.new_update = True
        x = list(set(self._jc_account.dev_list).intersection(set(data.keys())))
        if x:
            _LOGGER.warning("There is update for devices")
            for dev_id in x:
                self._jc_account.update_device(dev_id, data.get(dev_id))


def _execute_callback(callback, *args, **kwargs):
    # Callback with some data, capturing any exceptions to prevent chaos
    try:
        callback(*args, **kwargs)
    # pylint: disable=W0703
    except Exception as exc:
        _LOGGER.warning("Captured exception during callback: %s", exc)
