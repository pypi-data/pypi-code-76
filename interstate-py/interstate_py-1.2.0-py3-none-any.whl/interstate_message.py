from abc import abstractmethod, ABC
from enum import Enum
from typing import Dict, List


class InterstateWireMessageType(Enum):
    NEXT = "next"
    ERROR = "error"
    COMPLETE = "complete"
    PING = "ping"
    PONG = "pong"

    @staticmethod
    def header_key() -> str:
        return "message_type"

    @classmethod
    def header(cls, t) -> dict:
        return {cls.header_key(): t}


class InterstateWireMessage:

    def __init__(self, identity: bytes, header: Dict[str, str], payload: bytes):
        self._identity = identity
        self._header = header
        self._payload = payload
        self._type = self._determine_message_type(header)

    @property
    def header(self) -> Dict[str, str]:
        return self._header

    @property
    def payload(self) -> bytes:
        return self._payload

    @property
    def type(self) -> InterstateWireMessageType:
        return self._type

    @property
    def identity(self) -> bytes:
        return self._identity

    @property
    def identity_str(self):
        return self._identity.decode()

    def _determine_message_type(self, header: dict) -> InterstateWireMessageType:
        if InterstateWireMessageType.header_key() in header:
            message_type = header[InterstateWireMessageType.header_key()]
            if message_type == "connect":
                return InterstateWireMessageType.CONNECT
            elif message_type == "next":
                return InterstateWireMessageType.NEXT
            elif message_type == "error":
                return InterstateWireMessageType.ERROR
            elif message_type == "complete":
                return InterstateWireMessageType.COMPLETE
            elif message_type == "ping":
                return InterstateWireMessageType.PING
            elif message_type == "pong":
                return InterstateWireMessageType.PONG
            else:
                raise Exception("Received an unknown stream_type ('{}')".format(message_type))
        else:
            raise Exception("Could not determine message type - 'message_type' not present in header: {}".format(header))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, InterstateWireMessage):
            return False
        return self._header == o.header and self._payload == o.payload

    def __repr__(self) -> str:
        return "InterstateWireMessage(identity={}, type={}, header={}, payload={})".format(self._identity, self._type, self._header, self._payload)


class InterstateMessageAssembly(ABC):

    @staticmethod
    @abstractmethod
    def assemble(msg: InterstateWireMessage) -> List[bytes]:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def disassemble(msg: List[bytes]) -> List[bytes]:
        raise NotImplementedError()
