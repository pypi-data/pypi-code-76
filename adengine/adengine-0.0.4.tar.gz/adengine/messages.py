import abc
import base64
import json
import logging
import socket
import os
import tempfile

from .engine import ActivityData
from .pt import TopologyFilesNotSupported, WrongPassword, ActivityFileReadingError, ActivityNeedsPassword, \
    ExtractorError

__all__ = [
    'Message',
    'TaskMessage',
    'TaskIdMessage',
    'TaskIdNotFoundMessage',
    'TaskNotCompletedMessage',
    'QueueIsFullMessage',
    'ResultMessage',

    'send',
    'recv',

    'MessageError',
    'RecvError',
    'SendError',

    'DEFAULT_UNIX_SOCKET',
]

logger = logging.getLogger(f'adengine.messages')

BUFFER_SIZE = 1024
DEFAULT_UNIX_SOCKET = os.path.join(tempfile.gettempdir(), 'adengine/adengine.socket')


class MessageError(Exception):
    """Basic message exception."""
    pass


class SendError(Exception):
    """An error occured while sending message."""
    pass


class RecvError(Exception):
    """An error occurred while receiving message."""
    pass


class Message(abc.ABC):
    """Basic class representing message."""

    @abc.abstractmethod
    def _to_json(self) -> dict:
        """Converts object data to json."""
        pass

    def to_json(self) -> dict:
        """Combines _to_json return value with message type."""
        return {
            'message_type': self.__class__.__name__,
            'data': self._to_json(),
        }

    @classmethod
    @abc.abstractmethod
    def _from_json(cls, data: dict) -> 'Message':
        """Converts json to object data."""
        pass

    @classmethod
    def from_json(cls, data: dict) -> 'Message':
        """Retrieves json with object data from all json."""
        return cls._from_json(data['data'])

    def to_bytes(self):
        """Converts object to bytes."""
        return json.dumps(self.to_json()).encode('utf-8')

    @classmethod
    def from_bytes(cls, bytes_string: bytes) -> 'Message':
        """Creates object from bytes."""
        return cls.from_json(json.loads(bytes_string.decode('utf-8')))


class TaskMessage(Message):
    """Class representing message with task."""

    def __init__(self, activity: bytes, password: str or None, net_stabilization_delay: int):
        self._activity = activity
        self._password = password
        self._net_stabilization_delay = net_stabilization_delay

    def _to_json(self) -> dict:
        return {
            'password': self._password,
            'activity': base64.b64encode(self._activity).decode('utf-8'),
            'net_stabilization_delay': self._net_stabilization_delay,
        }

    @classmethod
    def _from_json(cls, data: dict) -> 'TaskMessage':
        return cls(
            base64.b64decode(data['activity'].encode('utf-8')),
            data['password'],
            data['net_stabilization_delay'],
        )

    @property
    def activity(self) -> bytes:
        return self._activity

    @property
    def password(self) -> str:
        return self._password

    @property
    def net_stabilization_delay(self) -> int:
        return self._net_stabilization_delay


class TaskIdNotFoundMessage(Message):
    """Class representing message with label that task id not found."""

    def _to_json(self) -> dict:
        return {}

    @classmethod
    def _from_json(cls, data: dict) -> 'TaskIdNotFoundMessage':
        return TaskIdNotFoundMessage()


class TaskNotCompletedMessage(Message):
    """Class representing message with label that task not competed."""

    def _to_json(self) -> dict:
        return {}

    @classmethod
    def _from_json(cls, data: dict) -> 'TaskNotCompletedMessage':
        return TaskNotCompletedMessage()


class QueueIsFullMessage(Message):
    """Class representing message with label that queue is full."""

    def _to_json(self) -> dict:
        return {}

    @classmethod
    def _from_json(cls, data: dict) -> 'QueueIsFullMessage':
        return QueueIsFullMessage()


class UnknownMessage(Message):
    """
    Class representing message which is send to client if received message
    is valid, but has not supported message type.
    """

    def _to_json(self) -> dict:
        return {}

    @classmethod
    def _from_json(cls, data: dict) -> 'UnknownMessage':
        return UnknownMessage()


class TaskIdMessage(Message):
    """Class representing message with task id."""

    def __init__(self, task_id: str):
        self._task_id = task_id

    def _to_json(self) -> dict:
        return {
            'task_id': self._task_id,
        }

    @classmethod
    def _from_json(cls, data: dict) -> 'TaskIdMessage':
        return cls(data['task_id'])

    @property
    def task_id(self) -> str:
        return self._task_id


class ResultMessage(Message):
    """Class representing result of task completion."""

    def __init__(self, activity_data: ActivityData):
        self._activity_data = activity_data

    def _to_json(self) -> dict:
        return {
            'error': self._activity_data.error.__class__.__name__ if self._activity_data.error else None,
            'data': self._activity_data.data,
        }

    @classmethod
    def _from_json(cls, data: dict) -> 'ResultMessage':
        return cls(
            ActivityData(
                cls._str2error(data['error']),
                data['data'],
            )
        )

    @property
    def activity_data(self) -> ActivityData:
        return self._activity_data

    @staticmethod
    def _error2str(error: ExtractorError) -> str:
        """Converts extractor error to string"""
        return error.__class__.__name__

    @staticmethod
    def _str2error(string: str) -> ExtractorError:
        """Converts string to extractor error"""
        errors = {error.__name__: error for error in (
            TopologyFilesNotSupported,
            WrongPassword,
            ActivityFileReadingError,
            ActivityNeedsPassword,
        )}
        return errors[string]() if string else None


def bytes2message(bytes_string: bytes):
    """Creates Message subclass from bytes."""
    messages = {message.__name__: message for message in (
        TaskMessage,
        TaskIdMessage,
        TaskIdNotFoundMessage,
        TaskNotCompletedMessage,
        QueueIsFullMessage,
        ResultMessage,
    )}
    message_type = json.loads(bytes_string.decode('utf-8'))['message_type']
    return messages[message_type].from_bytes(bytes_string)


def send(sock: socket.socket, message: Message):
    """Sends message using socket."""
    try:
        data = message.to_bytes()
        logger.debug(f'SEND data length: {len(data)}')
        data = len(data).to_bytes(8, byteorder='big', signed=False) + data
        sock.sendall(data)
        logger.debug(f'Sent message {message.__class__.__name__}')
    except Exception as e:
        raise SendError(e)


def recv(sock: socket.socket) -> bytes:
    """Receives message using socket."""
    try:
        total_bytes_num = int.from_bytes(sock.recv(8), byteorder='big', signed=False)
        logger.debug(f'RECEIVE data length: {total_bytes_num}')
        data = bytes()
        while len(data) != total_bytes_num:
            data += (sock.recv(BUFFER_SIZE))
        message = bytes2message(data)
        logger.debug(f'Received message {message.__class__.__name__}')
        return message
    except Exception as e:
        raise RecvError(e)
