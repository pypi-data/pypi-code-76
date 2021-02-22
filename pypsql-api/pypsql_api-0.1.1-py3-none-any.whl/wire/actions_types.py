import enum
from dataclasses import dataclass
from typing import Dict, Any

from pypsql_api.config.types import Session
from pypsql_api.ext.handlers import AuthHandler, QueryHandler
from pypsql_api.wire.bytes import ReadingIO, WritingIO


@dataclass
class Context:
    input: ReadingIO
    output: WritingIO

    session: Session

    auth_handler: AuthHandler
    query_handler: QueryHandler

    mem: Dict[str, Any]  # keep memory between tasks

    def update_mem(self, k, v):
        return Context(input=self.input, output=self.output,
                       session=self.session,
                       auth_handler=self.auth_handler,
                       query_handler=self.query_handler,
                       mem={**self.mem, **{k: v}})


class Names(enum.Enum):
    ERROR = 0
    READ_SSL_REQUEST = 1
    WRITE_SSL_YES = 2
    WRITE_SSL_NO = 3

    WRITE_PLAIN_TEXT_PASSWORD_REQUEST = 4
    READ_PLAIN_TEXT_PASSWORD = 5

    READ_STARTUP_MESSAGE = 6

    CLOSE = 7

    READY_FOR_QUERY = 8
    WRITE_AUTH_OK = 9
    RECEIVE_COMMAND = 10  # after ready for query we wait for the next command
    SIMPLE_QUERY = 11

    WRITE_EMPTY_RESPONSE = 12
    WRITE_DATA_FRAME = 13
