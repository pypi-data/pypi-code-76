import argparse
import socket
import time
import logging
import json
import traceback
import os

from .engine import QueueIsFull, TaskIdNotFound, TaskNotCompleted, ActivityData
from .messages import *

logger = logging.getLogger('adengine.client')

ADENGINE_UNIX_SOCK = os.environ.get('ADENGINE_UNIX_SOCK') or DEFAULT_UNIX_SOCKET


class Client:
    """Class representing client for ADEngine server."""
    def __init__(self, unix_socket: str):
        self._unix_socket = unix_socket

    def put(self, activity: bytes, password: str or None, activity_type: ActivityTypes) -> str:
        """Puts task to queue."""
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self._unix_socket)
        send(sock, TaskMessage(activity, password, activity_type))
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


def parse_args() -> dict:
    parser = argparse.ArgumentParser('ADEngine client')
    parser.add_argument('activity',
                        help='Path to activity file')
    parser.add_argument('-p', '--password',
                        help='Password for activity file',
                        dest='password',
                        default=None)
    parser.add_argument('-at', '--activity_type',
                        help='Activity type',
                        dest='activity_type',
                        type=ActivityTypes,
                        choices=ActivityTypes,
                        default=ActivityTypes.SMALL)
    parser.add_argument('-ux', '--unix_socket',
                        help='Path to unix socket',
                        dest='unix_socket',
                        default=ADENGINE_UNIX_SOCK)
    return vars(parser.parse_args())


def main() -> int:
    args = parse_args()
    client = Client(args['unix_socket'])

    with open(args['activity'], 'rb') as file:
        activity = file.read()

    try:
        try:
            task_id = client.put(activity, args['password'], args['activity_type'])
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
                        data = {
                            'consumed_time': str(result.consumed_time),
                            'data': result.data,
                        }
                        logger.info(json.dumps(data, indent=4))
    except Exception as e:
        logger.error(f'An error occurred :\n'
                     f'{traceback.format_exception(e.__class__, e, e.__traceback__)}')
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
