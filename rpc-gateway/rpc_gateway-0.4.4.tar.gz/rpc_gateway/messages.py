from typing import Any, List, Dict
from dataclasses import dataclass, asdict
import json
import pickle
from rpc_gateway import errors


class Encoding:
    PICKLE = 'pickle'
    JSON = 'json'


class Status:
    SUCCESS = 0
    ERROR = 1
    METHOD = 2
    PROXY = 3
    NOT_FOUND = 4
    LOCKED = 5


class Method:
    GET = 'get'
    SET = 'set'
    CALL = 'call'
    REGISTER = 'register'
    DEREGISTER = 'deregister'
    LOCK = 'lock'
    UNLOCK = 'unlock'
    AVAILABLE = 'available'
    METADATA = 'metadata'
    LIST = 'list'


@dataclass
class Message:
    id: int = 0
    data: Any = None
    encoding: str = Encoding.PICKLE


@dataclass
class Response(Message):
    status: int = Status.SUCCESS


@dataclass
class Request(Message):
    method: str = Method.GET


def decode(message_bytes: bytes) -> Message:
    # check for JSON message
    if message_bytes[0:1] in (b'{', '{'):  # use a slice instead of a normal index in case this is a bytes list
        message_data = json.loads(message_bytes)

        if 'status' in message_data:
            return Response(**message_data, encoding=Encoding.JSON)

        if 'method' in message_data:
            return Request(**message_data, encoding=Encoding.JSON)

        raise errors.InvalidMessageError(f'Invalid JSON message, no "status" or "method" keys found: {message_bytes}')

    # assume the message is using the pickle format if it's not JSON
    return pickle.loads(message_bytes)


def encode(message: Message) -> bytes:
    if message.encoding == Encoding.PICKLE:
        return pickle.dumps(message)

    json_dict = asdict(message)

    if 'encoding' in json_dict:
        json_dict.pop('encoding')

    return json.dumps(json_dict).encode()
