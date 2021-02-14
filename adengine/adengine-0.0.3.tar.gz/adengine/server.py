import os
import argparse
import datetime
import socket
import logging
import traceback
import json
import jsonschema

from .engine import Scheduler, TaskNotCompleted, TaskIdNotFound, QueueIsFull
from .messages import *

logger = logging.getLogger('adengine.server')

ADENGINE_UNIX_SOCK = os.environ.get('ADENGINE_UNIX_SOCK', None) or DEFAULT_UNIX_SOCKET
ADENGINE_ACTIVITY_TYPES_CONFIG = os.environ.get('ADENGINE_ACTIVITY_TYPES_CONFIG', None)

EXTRACT_TIMEOUT_FIELDNAME = 'extract_timeout'
NET_STABILIZATION_FIELDNAME = 'net_stabilization_delay'

ACTIVITY_TYPES_SCHEMA = {
    'type': 'object',
    'properties': {
        activity_type.value: {
            'type': 'object',
            'properties': {
                EXTRACT_TIMEOUT_FIELDNAME: {
                    'type': 'integer',
                    'minium': 5,
                    'maximum': 300,
                },
                NET_STABILIZATION_FIELDNAME: {
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 600,
                }
            },
            'required': [EXTRACT_TIMEOUT_FIELDNAME, NET_STABILIZATION_FIELDNAME],
            'maxProperties': 2,
        } for activity_type in ActivityTypes
    },
    'required': [activity_type.value for activity_type in ActivityTypes],
    'maxProperties': len(ActivityTypes),
}


def parse_timedelta(time_str: str):
    """Converts string hh:mm:ss to timedelta."""
    parts = time_str.split(':')
    time_params = dict(zip(['hours', 'minutes', 'seconds'],
                           (int(part) for part in parts)))
    return datetime.timedelta(**time_params)


def read_activity_types_config(filepath: str or None) -> dict:
    """Reads activity types config."""
    if not filepath:
        raise ValueError('Path to activity types config not specified')
    elif not os.path.isfile(filepath):
        raise FileNotFoundError('Activity types config not found')
    else:
        with open(filepath, 'r') as file:
            data = json.load(file)
        jsonschema.validate(data, ACTIVITY_TYPES_SCHEMA, jsonschema.Draft7Validator)
        return data


def parse_args() -> dict:
    parser = argparse.ArgumentParser('ADEngine server')
    parser.add_argument('-qs', '--queue-size',
                        help='Maximum size of the queue with tasks',
                        dest='queue_size',
                        type=int,
                        default=20)
    parser.add_argument('-wn', '--workers-num',
                        help='Number of workers',
                        dest='workers_num',
                        type=int,
                        default=1)
    parser.add_argument('-vd', '--virtual-display',
                        help='Use virtual display',
                        dest='virtual_display',
                        action='store_true')
    parser.add_argument('-rt', '--result-ttl',
                        help='Result ttl like hh:mm:ss',
                        dest='result_ttl',
                        type=parse_timedelta,
                        default=datetime.timedelta(minutes=5))
    parser.add_argument('-tb', '--tasks-before-session-restart',
                        help='Number of tasks before restarting PacketTracer session',
                        dest='tasks_before_session_restart',
                        type=int,
                        default=100)
    parser.add_argument('-us', '--unix-socket',
                        help='Path to unix socket',
                        dest='unix_socket',
                        default=ADENGINE_UNIX_SOCK)
    parser.add_argument('-mc', '--max-connections',
                        help='Maximum number of connections to server',
                        dest='max_connections',
                        type=int,
                        default=10)
    parser.add_argument('-at', '--activity_types_config',
                        help='Path to config with activity types',
                        dest='activity_types_config',
                        default=ADENGINE_ACTIVITY_TYPES_CONFIG)
    return vars(parser.parse_args())


def main():
    args = parse_args()

    try:
        activity_types = read_activity_types_config(args['activity_types_config'])
    except Exception as e:
        logger.error(f'Failed to read activity types config: '
                     f'{"".join(traceback.format_exception(e.__class__, e, e.__traceback__))}')
        exit(1)
    else:
        logger.info(f'Activity types:\n{json.dumps(activity_types, indent=4)}')

    unix_socket_path = args['unix_socket']
    if os.path.exists(unix_socket_path):
        logger.info(f'Unix socket {unix_socket_path} already_exists, remove it')
        os.remove(unix_socket_path)

    os.makedirs(os.path.dirname(unix_socket_path), exist_ok=True)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(unix_socket_path)

    returncode = 0

    logger.info('Starting scheduler...')
    with Scheduler(
            args['queue_size'],
            args['workers_num'],
            args['virtual_display'],
            args['result_ttl'],
            args['tasks_before_session_restart'],
    ) as scheduler:

        sock.listen(args['max_connections'])
        logger.info(f'Listening on unix socket: {unix_socket_path}...')
        while True:
            try:
                conn, _ = sock.accept()
                try:
                    message = recv(conn)
                except RecvError as e:
                    logger.error(f'An error occurred while receiving message:\n'
                                 f'{traceback.format_exception(RecvError, e, e.__traceback__)}')

                if isinstance(message, TaskMessage):
                    timeouts = activity_types[message.activity_type.value]
                    extract_timeout = datetime.timedelta(seconds=timeouts[EXTRACT_TIMEOUT_FIELDNAME])
                    net_stabilization_delay = datetime.timedelta(seconds=timeouts[NET_STABILIZATION_FIELDNAME])
                    try:
                        task_id = scheduler.put(message.activity,
                                                message.password,
                                                extract_timeout,
                                                net_stabilization_delay)
                    except QueueIsFull:
                        send(conn, QueueIsFullMessage())
                    else:
                        send(conn, TaskIdMessage(task_id))

                elif isinstance(message, TaskIdMessage):
                    try:
                        result = scheduler.get(message.task_id)
                    except TaskIdNotFound:
                        send(conn, TaskIdNotFoundMessage())
                    except TaskNotCompleted:
                        send(conn, TaskNotCompletedMessage())
                    else:
                        send(conn, ResultMessage(result))

                conn.close()

            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f'Unexpected exception:\n'
                             f'{"".join(traceback.format_exception(e.__class__, e, e.__traceback__))}')
                break

        logger.info('Stop server...')

    return returncode


if __name__ == '__main__':
    exit(main())
