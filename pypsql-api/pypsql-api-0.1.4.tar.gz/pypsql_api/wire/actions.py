from pypsql_api.config.types import Session
from pypsql_api.wire.actions_types import Context, Names
from pypsql_api.wire.back import SSLNo, AuthenticationCleartextPassword, ReadyForQuery, AuthenticationOk, \
    EmptyQueryResponse, DataFrameRowDescription, DataFrameDataRows, CommandComplete
from pypsql_api.wire.front import SSLRequest, StartupMessage, Message, PasswordMessage


def read_ssl_request(context: Context):
    ssl_request = SSLRequest.read(context.input)

    return context.update_mem('ssl_request', ssl_request), Names.WRITE_SSL_NO


def write_ssl_resp_no(context: Context):
    SSLNo().write(context.output)

    return context, Names.READ_STARTUP_MESSAGE


def read_startup_message(context: Context):
    startup_front = StartupMessage.read(context.input)

    print(f"Got startup  {startup_front}")

    session = Session(
        user=startup_front.user, database=startup_front.database, password=''
    )

    context.session = session
    return context.update_mem('session', session), Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST


def write_plain_text_password_request(context: Context):
    AuthenticationCleartextPassword().write(context.output)
    context.output.flush()

    return context, Names.READ_PLAIN_TEXT_PASSWORD


def read_plain_text_password_request(context: Context):
    m, t = Message.read(context.input)

    if not (m and t):
        return context, None

    if not isinstance(m, PasswordMessage):
        raise Exception(f"UnExpected message {m}")

    session = context.session
    session.password = m.password

    auth_ok, msg = context.auth_handler.handle(session=session)

    if auth_ok:
        return context, Names.WRITE_AUTH_OK
    else:
        raise Exception(f"Password not correct {msg}")


def write_ready_for_query(context: Context):
    ReadyForQuery().write(context.output)
    context.output.flush()

    return context, Names.RECEIVE_COMMAND


def write_auth_ok(context: Context):
    AuthenticationOk().write(context.output)
    context.output.flush()

    return context, Names.READY_FOR_QUERY


def read_receive_command(context: Context):
    m, t = Message.read(context.input)

    print(f">>read_receive_command msg {m}, {t}")
    if not (m and t):
        return context, None

    return context.update_mem('message', m), m.process_name


def write_empty_response(context: Context):
    EmptyQueryResponse().write(context.output)

    return context, Names.READY_FOR_QUERY


def write_data_frame_response(context: Context):
    df = context.mem['data']
    if df is None:
        raise Exception("We expect a data frame instance here")

    DataFrameRowDescription(df=df).write(context.output)
    rows = DataFrameDataRows(df=df).write(context.output)
    CommandComplete(tag=f"SELECT {rows}").write(context.output)

    context.output.flush()

    return context, Names.READY_FOR_QUERY
