from typing import Any

from interstate_py.interstate_message import InterstateWireMessageType


class MultiplexMessage:
    """
    A unpacked messages containing the deserialized payload.
    """
    def __init__(self, identity: str, type: InterstateWireMessageType, payload: Any):
        self._identity = identity
        self._type = type
        self._payload = payload

    @property
    def identity(self) -> str:
        return self._identity

    @property
    def type(self) -> InterstateWireMessageType:
        return self._type

    @property
    def payload(self):
        return self._payload

    def __repr__(self) -> str:
        return "MultiplexMessage(identity={}, type={})".format(self._identity, self._type)

