# see: https://docs.python.org/3/library/socketserver.html
import socketserver
from abc import abstractmethod, ABC
from typing import Tuple, Optional, Union, Any

from pandas import DataFrame

from pypsql_api.config.types import Session
from pypsql_api.ext.handlers import AuthHandler, QueryHandler
from pypsql_api.wire.actions_types import Context, Names
from pypsql_api.wire.back import ErrorResponse
from pypsql_api.wire.bytes import ReadingIO, WritingIO
from pypsql_api.wire.protocol import run_states


def state_runner(existing_state, message_processor):
    state = message_processor.next(existing_state)
    message_processor.is_allowed(state)

    return state


class PsqlHandler(ABC, socketserver.StreamRequestHandler, socketserver.ThreadingMixIn):

    @property
    @abstractmethod
    def auth_handler_cls(self):
        raise Exception("Not implemented")

    @property
    @abstractmethod
    def query_handler_cls(self):
        raise Exception("Not implemented")

    def handle(self):

        input = ReadingIO(self.rfile)
        output = WritingIO(self.wfile)

        try:
            context = Context(
                input=input,
                output=output,
                mem={},

                auth_handler=self.auth_handler_cls(),
                query_handler=self.query_handler_cls(),
                session=None,
            )

            state_name = Names.READ_SSL_REQUEST

            context, state_name = run_states(context, state_name)


        except Exception as e:
            print(e)
            ErrorResponse.severe(str(e)).write(output)

            raise e

        finally:
            output.close()

        print("End")


def run(auth_handler_cls, query_handler_cls, handler=None, host="", port=55432):
    auth_1 = auth_handler_cls
    query_1 = query_handler_cls

    if not handler:
        class Handler(PsqlHandler):
            auth_handler_cls = auth_1
            query_handler_cls = query_1

        handler = Handler

    with socketserver.TCPServer((host, port), handler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print(f"Running postgresql server on {host}:{port}")
        server.serve_forever()


if __name__ == "__main__":

    class TestAuth(AuthHandler):

        def handle(self, session: Session) -> Tuple[bool, Optional[str]]:
            if session.password == "test":
                return True, None

            return False, None


    class QueryHandler(QueryHandler):

        def handle(self, session: Session, sql) -> Tuple[Optional[Union[Any, Optional[DataFrame]]], Optional[Any]]:
            import pandas as pd
            import datetime
            import numpy as np
            from decimal import Decimal
            print(f"Handling query {sql}")
            return pd.DataFrame({'id': [1.232323,2.1233,np.nan], 'name': [1,2,3],
                                 'p': [Decimal(1212323213123), Decimal(121312312321321323121321312321312323213), Decimal(123123213213213213213)]}), None


    run(auth_handler_cls=TestAuth, query_handler_cls=QueryHandler)
