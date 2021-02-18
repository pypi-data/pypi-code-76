import pytest
import sys
import subprocess
import signal
import datetime
import os
import time
import tempfile
import multiprocessing as mp
import itertools

from adengine.client import Client
from adengine.engine import TaskIdNotFound, TaskNotCompleted, QueueIsFull, ActivityData
from adengine.pt import WrongPassword, ActivityFileReadingError, ActivityNeedsPassword, TopologyFilesNotSupported

from test import TEST_DATA, USE_VIRTUAL_DISPLAY, READ_FILE_TIMEOUT, read_file_binary

QUEUE_SIZE = 10
WORKERS_NUM = 2
RESULT_TTL = datetime.timedelta(hours=1)
TASKS_BEFORE_SESSION_RESTART = 100
MAX_CONNECTIONS = QUEUE_SIZE
UNIX_SOCKET = os.path.join(tempfile.gettempdir(), 'adengine_test/adengine.socket')


@pytest.fixture(scope='module', autouse=True)
def server():
    cmd = [
        sys.executable,
        '-m', 'adengine.server',
        '--queue-size', str(QUEUE_SIZE),
        '--workers-num', str(WORKERS_NUM),
        '--read-file-timeout', str(READ_FILE_TIMEOUT),
        '--virtual-display' if USE_VIRTUAL_DISPLAY else '',
        '--result-ttl', str(RESULT_TTL),
        '--tasks-before-session-restart', str(TASKS_BEFORE_SESSION_RESTART),
        '--max-connections', str(MAX_CONNECTIONS),
        '--unix-socket', UNIX_SOCKET,
    ]
    process = subprocess.Popen(cmd)
    time.sleep(1)
    yield
    process.send_signal(signal.SIGINT)
    process.wait()


@pytest.fixture(scope='function')
def client():
    return Client(UNIX_SOCKET)


def test_client_normal(client):
    tasks = [
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'),
        (read_file_binary(os.path.join(TEST_DATA, 'without_password.pka')), None),
    ]

    task_ids = [client.put(activity, password) for activity, password in tasks]
    sleep_delta = 1
    while len(task_ids):
        time.sleep(sleep_delta)
        for task_id in tuple(task_ids):
            try:
                activity_data = client.get(task_id)
            except TaskNotCompleted:
                pass
            else:
                task_ids.remove(task_id)
                assert activity_data.data


def test_client_errors(client):
    tasks = [
        ('no_such_file.pka'.encode('utf-8'), 'password', ActivityFileReadingError),
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), 'wrong_password', WrongPassword),
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), None, ActivityNeedsPassword),
        (read_file_binary(os.path.join(TEST_DATA, 'topology.pkt')), None, TopologyFilesNotSupported),
    ]

    task_ids = {client.put(activity, password): error_type for activity, password, error_type in tasks}
    sleep_delta = 1
    while len(task_ids):
        time.sleep(sleep_delta)
        for task_id in tuple(task_ids):
            try:
                activity_data = client.get(task_id)
            except TaskNotCompleted:
                pass
            else:
                error_type = task_ids.pop(task_id)
                assert isinstance(activity_data.error, error_type)


def test_queue_is_full(client):
    activity, password = read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'
    tasks = []
    with pytest.raises(QueueIsFull):
        for i in range(QUEUE_SIZE * 2):
            tasks.append(client.put(activity, password))

    sleep_delta = 1
    while len(tasks):
        time.sleep(sleep_delta)
        for task_id in tuple(tasks):
            try:
                result = client.get(task_id)
            except TaskNotCompleted:
                pass
            else:
                tasks.remove(task_id)
                assert result.data


def test_task_id_not_found(client):
    with pytest.raises(TaskIdNotFound):
        client.get('no_such_task_id')


def test_task_not_completed(client):
    activity, password = read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'
    task_id = client.put(activity, password)
    with pytest.raises(TaskNotCompleted):
        client.get(task_id)


def extract_data(activity: bytes, password: str or None) -> ActivityData:
    client = Client(UNIX_SOCKET)
    task_id = client.put(activity, password)
    while True:
        time.sleep(1)
        try:
            result = client.get(task_id)
        except TaskNotCompleted:
            continue
        else:
            return result


def test_process_safe():
    activity, password = read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'
    tasks_num = WORKERS_NUM * 4

    with mp.Pool(WORKERS_NUM) as pool:
        result = pool.starmap(extract_data, itertools.repeat((activity, password), tasks_num))

    for activity_data in result:
        assert activity_data.data


@pytest.mark.parametrize(
    ['activity', 'password', 'net_stabilization_delay', 'total_percentage'],
    [
        pytest.param(
            read_file_binary(os.path.join(TEST_DATA, 'with_net_stabilization_delay_small.pka')),
            '123', 5, 0.0, id='small'
        ),
        pytest.param(
            read_file_binary(os.path.join(TEST_DATA, 'with_net_stabilization_delay_big.pka')),
            '123', 20, 97.0, id='big'
        ),
    ]

)
def test_net_stabilization_delay(client, activity, password, net_stabilization_delay, total_percentage):
    task_id = client.put(activity, password, net_stabilization_delay)
    activity_data = None
    while not activity_data:
        try:
            activity_data = client.get(task_id)
        except TaskNotCompleted:
            time.sleep(0.5)
    assert abs(activity_data.data['totalPercentage'] - total_percentage) < 1.0
