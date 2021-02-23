import io
import time
from dataclasses import dataclass
from typing import Any, Optional, Tuple

from pypsql_api.wire.actions_types import Names
from pypsql_api.wire.bytes import ReadingIO


@dataclass
class SSLRequest:
    request_code: int

    @staticmethod
    def read(buff: ReadingIO):
        inner_buff, message_len = buff.read_int32_delim_message()
        return SSLRequest(request_code=inner_buff.read_int32())


@dataclass
class StartupMessage:
    protocol_version: int
    user: str
    database: str
    options: str

    @staticmethod
    def read(buff: ReadingIO):
        inner_buff, message_len = buff.read_int32_delim_message()

        if not inner_buff:
            raise Exception("Invalid startup message, the length must be > 4 bytes")

        protocol_version = inner_buff.read_int32()
        message_len -= 4
        d = {}

        if message_len > 0:
            while True:
                n = inner_buff.read_cstring()
                if not n:
                    break
                v = inner_buff.read_cstring()
                if not v:
                    break

                d[n] = v

        return StartupMessage(
            protocol_version=protocol_version, user=d.get('user', ''), database=d.get('database', ''),
            options=d.get('options', '')
        )


@dataclass
class PasswordMessage:
    password: str

    @staticmethod
    def read_body(buff: ReadingIO):
        return PasswordMessage(password=buff.read_cstring())


@dataclass
class QueryMessage:
    query: str

    process_name: Any = Names.SIMPLE_QUERY

    @staticmethod
    def read_body(buff: ReadingIO):
        return QueryMessage(query=buff.read_cstring())


@dataclass
class Terminate:
    process_name: Any = Names.CLOSE

    @staticmethod
    def read_body(_: ReadingIO):
        return Terminate()


message_type_map = {
    ord('p'): PasswordMessage.read_body,
    ord('Q'): QueryMessage.read_body,
    ord('X'): Terminate.read_body,
}


class Message:

    @staticmethod
    def read(buff: ReadingIO) -> Tuple[Optional[Any], Optional[bytes]]:
        """
        Returns [Optional[Message], type:bytes
        If The message and Type are None, we've reached the end of stream
        """

        t = buff.read_byte()

        if not t:
            return None, None

        fn = message_type_map.get(ord(t), None)
        if fn:
            try:
                inner_buff, _ = buff.read_int32_delim_message()
                return fn(inner_buff), t
            except Exception as e:
                return fn(io.BytesIO()), t

        return None, t
