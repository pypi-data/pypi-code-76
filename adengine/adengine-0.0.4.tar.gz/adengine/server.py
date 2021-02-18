import os
import argparse
import datetime
import socket
import logging
import traceback

from .engine import Scheduler, TaskNotCompleted, TaskIdNotFound, QueueIsFull
from .messages import *

logger = logging.getLogger('adengine.server')

ADENGINE_UNIX_SOCK = os.environ.get('ADENGINE_UNIX_SOCK', None) or DEFAULT_UNIX_SOCKET


def parse_timedelta(time_str: str):
    """Converts string hh:mm:ss to timedelta."""
    try:
        parts = time_str.split(':')
        time_params = dict(zip(['hours', 'minutes', 'seconds'],
                               (int(part) for part in parts)))
        return datetime.timedelta(**time_params)
    except Exception as e:
        raise ValueError(e)


def parse_positive_int(value: str):
    value = int(value)
    if value < 0:
        raise ValueError('Value must be positive')
    return value


def parse_read_file_timeout(min_file_read_timeout: int, max_file_read_timeout: int):
    def _parse_read_file_timeout(value: str):
        value = int(value)
        if value < min_file_read_timeout or value > max_file_read_timeout:
            raise ValueError(f'File reading timeout must not be lower than {min_file_read_timeout} '
                             f'and not greater than {max_file_read_timeout}')
    return _parse_read_file_timeout


def parse_args() -> dict:
    parser = argparse.ArgumentParser('ADEngine server')
    parser.add_argument('--queue-size',
                        help='Maximum size of the queue with tasks',
                        dest='queue_size',
                        type=parse_positive_int,
                        default=20)
    parser.add_argument('--workers-num',
                        help='Number of workers',
                        dest='workers_num',
                        type=parse_positive_int,
                        default=1)
    parser.add_argument('--read-file-timeout',
                        help='Timout for reading activity file (in seconds)',
                        dest='read_file_timeout',
                        type=parse_read_file_timeout(5, 60),
                        default=5)
    parser.add_argument('--virtual-display',
                        help='Use virtual display',
                        dest='virtual_display',
                        action='store_true')
    parser.add_argument('--result-ttl',
                        help='Result ttl like hh:mm:ss',
                        dest='result_ttl',
                        type=parse_timedelta,
                        default=datetime.timedelta(minutes=5))
    parser.add_argument('--tasks-before-session-restart',
                        help='Number of tasks before restarting PacketTracer session',
                        dest='tasks_before_session_restart',
                        type=parse_positive_int,
                        default=100)
    parser.add_argument('--unix-socket',
                        help='Path to unix socket',
                        dest='unix_socket',
                        default=ADENGINE_UNIX_SOCK)
    parser.add_argument('--max-connections',
                        help='Maximum number of connections to server',
                        dest='max_connections',
                        type=parse_positive_int,
                        default=10)
    return vars(parser.parse_args())


def main():
    args = parse_args()

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
            args['read_file_timeout'],
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
                    try:
                        task_id = scheduler.put(message.activity,
                                                message.password,
                                                message.net_stabilization_delay)
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
