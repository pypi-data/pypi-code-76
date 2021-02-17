import time
from dataclasses import dataclass
from typing import Callable, Set, Tuple, Any

from pypsql_api.wire.actions import write_ssl_resp_no, read_startup_message, read_plain_text_password_request, \
    write_plain_text_password_request, read_ssl_request, write_ready_for_query, write_auth_ok, read_receive_command, \
    write_empty_response, write_data_frame_response
from pypsql_api.wire.actions_types import Names
from pypsql_api.wire.query.simple_query import process_simple_query


@dataclass
class State:
    allowed: Set[str]
    name: str
    fn: Callable[[Any], Tuple[Any, str]]

    def move_next(self, context: Any):
        return self.fn(context)


def move_state(context: Any, state: State) -> Tuple[Any, str]:
    ctx_new, new_state = state.move_next(context)

    if not new_state:
        return ctx_new, Names.CLOSE

    if not new_state in state.allowed:
        raise Exception(f"Invalid state {new_state} from {state.name}, allowed states are {state.allowed}")

    return ctx_new, new_state


processes = {
    Names.READ_SSL_REQUEST: State(name=Names.READ_SSL_REQUEST, allowed={Names.WRITE_SSL_NO}, fn=read_ssl_request),
    Names.WRITE_SSL_NO: State(name=Names.READ_SSL_REQUEST, allowed={Names.READ_STARTUP_MESSAGE}, fn=write_ssl_resp_no),
    Names.READ_STARTUP_MESSAGE: State(name=Names.READ_STARTUP_MESSAGE,
                                      allowed={Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST}, fn=read_startup_message),

    Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST: State(name=Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST,
                                                   allowed={Names.READ_PLAIN_TEXT_PASSWORD},
                                                   fn=write_plain_text_password_request),

    Names.READ_PLAIN_TEXT_PASSWORD: State(name=Names.READ_PLAIN_TEXT_PASSWORD,
                                          allowed={Names.CLOSE, Names.WRITE_AUTH_OK},
                                          fn=read_plain_text_password_request),

    Names.WRITE_AUTH_OK: State(name=Names.READ_PLAIN_TEXT_PASSWORD,
                               allowed={Names.READY_FOR_QUERY},
                               fn=write_auth_ok),

    Names.READY_FOR_QUERY: State(name=Names.READY_FOR_QUERY,
                                 allowed={Names.CLOSE, Names.RECEIVE_COMMAND}, fn=write_ready_for_query),

    Names.RECEIVE_COMMAND: State(name=Names.RECEIVE_COMMAND,
                                 allowed={Names.CLOSE, Names.READY_FOR_QUERY, Names.SIMPLE_QUERY},
                                 fn=read_receive_command),

    Names.SIMPLE_QUERY: State(name=Names.SIMPLE_QUERY,
                              allowed={Names.CLOSE, Names.READY_FOR_QUERY, Names.WRITE_EMPTY_RESPONSE, Names.WRITE_DATA_FRAME},
                              fn=process_simple_query),

    Names.WRITE_EMPTY_RESPONSE: State(name=Names.WRITE_EMPTY_RESPONSE,
                                      allowed={Names.CLOSE, Names.READY_FOR_QUERY},
                                      fn=write_empty_response),

    Names.WRITE_DATA_FRAME: State(name=Names.WRITE_DATA_FRAME,
                                      allowed={Names.CLOSE, Names.READY_FOR_QUERY},
                                      fn=write_data_frame_response)

}


def run_states(context, state_name):
    while state_name != Names.CLOSE:
        print(f"Running state {state_name}")
        state = processes.get(state_name)

        context, state_name = move_state(context, state)

        if not state_name:
            state_name = Names.CLOSE

    print("End run states")

    return context, state_name
