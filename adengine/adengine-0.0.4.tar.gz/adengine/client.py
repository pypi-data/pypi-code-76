import argparse
import socket
import time
import logging
import json
import traceback
import os
import stat

from .engine import QueueIsFull, TaskIdNotFound, TaskNotCompleted, ActivityData
from .messages import *

logger = logging.getLogger('adengine.client')

ADENGINE_UNIX_SOCK = os.environ.get('ADENGINE_UNIX_SOCK') or DEFAULT_UNIX_SOCKET


class Client:
    """Class representing client for ADEngine server."""
    def __init__(self, unix_socket: str):
        self._unix_socket = unix_socket

    def put(self, activity: bytes, password: str or None, net_stabilization_delay=0) -> str:
        """Puts task to queue."""
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self._unix_socket)
        send(sock, TaskMessage(activity, password, net_stabilization_delay))
        message = recv(sock)
        sock.close()

        if isinstance(message, QueueIsFullMessage):
            raise QueueIsFull
        elif isinstance(message, TaskIdMessage):
            return message.task_id

    def get(self, task_id: str) -> ActivityData:
        """Gets task result."""
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self._unix_socket)
        send(sock, TaskIdMessage(task_id))
        message = recv(sock)
        sock.close()

        if isinstance(message, TaskIdNotFoundMessage):
            raise TaskIdNotFound
        elif isinstance(message, TaskNotCompletedMessage):
            raise TaskNotCompleted
        elif isinstance(message, ResultMessage):
            return message.activity_data


def parse_net_stabilization_delay(min_net_stabilization_delay: int, max_net_stabilization_delay: int):
    def _parse_net_stabilization_delay(value: str):
        value = int(value)
        if value < min_net_stabilization_delay or value > max_net_stabilization_delay:
            raise ValueError(f'Network stabilization delay must not be lower than {min_net_stabilization_delay} '
                             f'and not greater than {max_net_stabilization_delay}')
    return _parse_net_stabilization_delay


def parse_existing_file(value: str):
    if not os.path.isfile(value):
        raise ValueError('File not exists')
    return value


def parse_unix_socket(value: str):
    if not os.path.exists(value):
        raise ValueError('Socket not exists')
    mode = os.stat(value).st_mode
    if not stat.S_ISSOCK(mode):
        raise ValueError('File is not unix socket')
    return value


def parse_args() -> dict:
    parser = argparse.ArgumentParser('ADEngine client')
    parser.add_argument('activity',
                        help='Path to activity file',
                        type=parse_existing_file)
    parser.add_argument('--password',
                        help='Password for activity file',
                        dest='password',
                        default=None)
    parser.add_argument('--net-stabilization-delay',
                        help='Network stabilization delay (in seconds)',
                        dest='net_stabilization_delay',
                        type=parse_net_stabilization_delay(0, 600),
                        default=0)
    parser.add_argument('--socket',
                        help='Path to unix socket',
                        dest='socket',
                        type=parse_unix_socket,
                        default=ADENGINE_UNIX_SOCK)
    return vars(parser.parse_args())


def main() -> int:
    args = parse_args()
    client = Client(args['socket'])

    with open(args['activity'], 'rb') as file:
        activity = file.read()

    try:
        try:
            task_id = client.put(activity, args['password'], args['net_stabilization_delay'])
        except QueueIsFull:
            logger.info('Queue is full')
            return 1
        else:
            result = None
            while not result:
                try:
                    result = client.get(task_id)
                except TaskNotCompleted:
                    logger.info('Task not ready')
                    time.sleep(0.5)
                    continue
                else:
                    logger.info(f'Task completed!')

                    if result.error:
                        logger.info(f'Error: {result.error.__class__.__name__}')
                    else:
                        logger.info(json.dumps(result.data, indent=4))
    except Exception as e:
        logger.error(f'An error occurred :\n'
                     f'{traceback.format_exception(e.__class__, e, e.__traceback__)}')
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
