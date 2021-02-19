import asyncio

import datetime
import os
import pickle
import pprint
import struct
import socket
import sys
import traceback

import click
from ps.basic import Config

from ps.herald import __version__
from ps.herald import database
from ps.herald import create_app
from ps.herald.model import Log


minimal_msg_fields = [
    "summary",
    "produkt_id",
    "system_id",
    "sub_system_id",
    "sub_sub_system_id",
    "user_spec_1",
    "user_spec_2",
    "api_version",
    "package_version",
]

CLIENTS = {}  # asynchronous tasks are "remembered here"

VERBOSE = False
BRIDGE_MODE = False
AGE = False
ROUND = 1024
SESSION = None
SOCKE = None


def client_connected_handler(client_reader, client_writer):
    """Start a new asyncio.Task to handle this specific client connection"""
    task = asyncio.Task(handle_client(client_reader, client_writer))
    CLIENTS[task] = (client_reader, client_writer)

    def client_done(task):
        """When the tasks that handles the specific client
        connection is done.
        """
        del CLIENTS[task]

    # Add the client_done callback to be run when the future becomes done
    task.add_done_callback(client_done)


@asyncio.coroutine
def handle_client(client_reader, client_writer):
    """Runs for each client connected.

    The first 4 bytes of the message define the total length of
    the message. Hence in the first step, the first four bytes are
    read and then the rest of the message. This "rest" of the message
    is depickled and stored in the database. If the "bridge-mode" is
    enabled, the "byte-buffer" (first 4 bytes plus the rest of the
    message is also sent to another socket - the bridge socket.
    """
    global SOCKE, SESSION, VERBOSE, BRIDGE_MODE, AGE, ROUND
    current_round = 0
    session = database.get_session()
    # Config.logger.debug("new client connected", extra={"package_version": __version__})
    new_connection = True
    while True:
        if VERBOSE:
            print(f"Got msg new_connection is {new_connection}")
        current_round += 1
        data1 = yield from (client_reader.read(4))
        if not data1:
            break
        if len(data1) < 4:
            print("Did not receive First 4 Bytes of message")
            raise AttributeError
        slen = struct.unpack(">L", data1)[0]
        data2 = yield from (client_reader.read(slen))
        if BRIDGE_MODE:
            print_to_tunnel(data1 + data2)
        obj = pickle.loads(data2)
        dt = datetime.datetime.now()
        obj["created"] = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        # make sure we have at list None values in the list
        # - some older python instances may drop values ...
        lowered_obj = {k: str(None) for k in minimal_msg_fields}

        try:
            for name, value in obj.items():
                if name == "msg":
                    name = "message"
                    value = value.replace("\u2018", " ").replace("\u2019", " ")
                    value = str(value).replace("'", " ").replace('"', " ")
                if name == "args":
                    value = ""
                if value is None:
                    lowered_obj[name.lower()] = str(value)
                else:
                    lowered_obj[name.lower()] = value
                if VERBOSE:
                    print(name.lower(), "    ", value)

            lowered_obj["summary"] = (
                str("None")
                + lowered_obj["produkt_id"]
                + lowered_obj["system_id"]
                + lowered_obj["sub_system_id"]
                + lowered_obj["sub_sub_system_id"]
                + lowered_obj["user_spec_1"]
                + lowered_obj["user_spec_2"]
            )
            if VERBOSE:
                print(pprint.pformat(lowered_obj))
            row = Log(**lowered_obj)
            session = database.get_session()
            session.add(row)
            session.commit()
            if new_connection:
                new_connection = False
                Config.logger.debug(
                    "new client connected from %s on %s "
                    % (lowered_obj["system_id"], lowered_obj["sub_system_id"]),
                    extra={"package_version": __version__},
                )

        except Exception as e:
            Config.logger.exception(
                "Error: while writing to database/elasticsearch",
                extra={"package_version": __version__},
            )
            print(lowered_obj)
            traceback.print_exc(e, file=sys.stderr)
            session.rollback()
            continue

        if VERBOSE:
            print("Added a row")
            # if lowered_obj["module]" != 'ps_bridge':
            #    Config.logger.debug(
            #    "row added", extra={"package_version": __version__}
            #   )
            sys.stdout.flush()
        if AGE and 0 == (current_round % ROUND):
            current_round = 0
            start_date = str(
                datetime.datetime.now() - datetime.timedelta(seconds=AGE)
            )
            to_del = Log.query.filter(Log.created < start_date).delete()
            sys.stdout.write("OK: %s rows deleted" % (to_del))


def print_to_tunnel(data_p):
    """Running in bridge-mode we route the incoming message to
    the outgoing socket."""
    global SOCKE
    try:
        SOCKE.sendall(data_p)
    except AttributeError:
        SOCKE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOCKE.connect(("", Config.logging_bridge_port))
        sys.stderr.write("Attribute Error: while writing to bridge-tunnel ")
    except Exception as e:
        sys.stderr.write("Error: while writing to bridge-tunnel ")
        Config.logger.exception("Error: while writing to bridge-tunnel ")
        traceback.print_exc(e, file=sys.stdout)
        SOCKE.close()
        SOCKE = None


@click.command()
@click.option(
    "--extra",
    "-x",
    is_flag=True,
    type=bool,
    default=False,
    help="internal tests only",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    type=bool,
    default=False,
    help="set verbose mode",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    type=bool,
    default=False,
    help="set debug mode",
)
@click.option(
    "--bridge",
    "-b",
    is_flag=True,
    type=bool,
    default=False,
    help="set bridge mode",
)
@click.option(
    "--rounds",
    "-r",
    type=int,
    help="check for messages to delete after that amount of inserts",
)
@click.option(
    "--seconds",
    "-s",
    type=int,
    help="delete messages older than age seconds while running \
        ( a week are 604800 seconds)",
)
def main(extra, verbose, debug, bridge, rounds, seconds):
    """
    The Bridge module receives messages emited with the Standard Python
    logging StreamHandler. These messages are stored in a database.
    The logging events lateron can be analyzed e.g. with the herald Server.

    To use the bridge-functionality it might be needed to establish a
    tunnel to another machine

    """
    global VERBOSE, BRIDGE_MODE, AGE, ROUND
    VERBOSE = verbose
    BRIDGE_MODE = bridge
    AGE = seconds
    ROUND = rounds

    click.echo("ps_bridge. Debug mode is %s" % ("on" if debug else "off"))
    if extra:
        return 0

    app = create_app("ps_bridge")
    Config.logger.debug("started", extra={"package_version": __version__})

    loop = asyncio.get_event_loop()
    sys.stdout.flush()
    print("will listen on %d" % (Config.logging_port))
    with app.app_context():
        if not os.path.isfile(Config.herald_sqlite_filename):
            database.init_db()
            print("Database initted")
            Config.logger.debug(
                "database initted,", extra={"package_version": __version__}
            )
        loop.run_until_complete(
            asyncio.start_server(
                client_connected_handler, "0.0.0.0", Config.logging_port
            )
        )
        try:
            loop.run_forever()
        finally:
            loop.close()


if __name__ == "__main__":
    sys.exit(main())
