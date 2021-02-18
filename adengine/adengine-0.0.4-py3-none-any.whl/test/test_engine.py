import pytest
import os
import time
import datetime
import threading
import typing

from adengine.engine import *
from adengine.pt import *

from test import TEST_DATA, USE_VIRTUAL_DISPLAY, READ_FILE_TIMEOUT, read_file_binary

QUEUE_SIZE = 10
WORKERS_NUM = 2
RESULT_TTL = datetime.timedelta(hours=1)
TASKS_BEFORE_RESTART = 100


@pytest.fixture(scope='module')
def launch_engine():
    scheduler = Scheduler(QUEUE_SIZE, WORKERS_NUM, READ_FILE_TIMEOUT, USE_VIRTUAL_DISPLAY, RESULT_TTL,
                          TASKS_BEFORE_RESTART)
    scheduler.start()
    yield scheduler
    scheduler.stop()


def test_engine_normal(launch_engine):
    tasks = [
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'),
        (read_file_binary(os.path.join(TEST_DATA, 'without_password.pka')), None),
    ]

    task_ids = [launch_engine.put(activity, password) for activity, password in tasks]
    sleep_delta = 1
    while len(task_ids):
        time.sleep(sleep_delta)
        for task_id in tuple(task_ids):
            try:
                activity_data = launch_engine.get(task_id)
            except TaskNotCompleted:
                pass
            else:
                task_ids.remove(task_id)
                assert activity_data.data


def test_engine_errors(launch_engine):
    tasks = [
        ('no_such_file.pka'.encode('utf-8'), 'password', ActivityFileReadingError),
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), 'wrong_password', WrongPassword),
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), None, ActivityNeedsPassword),
        (read_file_binary(os.path.join(TEST_DATA, 'topology.pkt')), None, TopologyFilesNotSupported),
    ]

    task_ids = {launch_engine.put(activity, password): error_type for
                activity, password, error_type in tasks}
    sleep_delta = 1
    while len(task_ids):
        time.sleep(sleep_delta)
        for task_id in tuple(task_ids):
            try:
                activity_data = launch_engine.get(task_id)
            except TaskNotCompleted:
                pass
            else:
                error_type = task_ids.pop(task_id)
                assert isinstance(activity_data.error, error_type)


def test_queue_is_full(launch_engine):
    activity, password = read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'
    tasks = []
    with pytest.raises(QueueIsFull):
        for i in range(QUEUE_SIZE * 2):
            tasks.append(launch_engine.put(activity, password))

    sleep_delta = 1
    while len(tasks):
        time.sleep(sleep_delta)
        for task_id in tuple(tasks):
            try:
                result = launch_engine.get(task_id)
            except TaskNotCompleted:
                pass
            else:
                tasks.remove(task_id)
                assert result.data


def test_task_id_not_found(launch_engine):
    with pytest.raises(TaskIdNotFound):
        launch_engine.get('no_such_task_id')


def test_task_not_completed(launch_engine):
    activity, password = read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'
    task_id = launch_engine.put(activity, password)
    with pytest.raises(TaskNotCompleted):
        launch_engine.get(task_id)


def test_result_ttl():
    activity, password = read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'
    result_ttl = datetime.timedelta(seconds=READ_FILE_TIMEOUT * 2)
    workers_num = 1

    with Scheduler(QUEUE_SIZE, workers_num, READ_FILE_TIMEOUT, USE_VIRTUAL_DISPLAY, result_ttl) as scheduler:
        old_task_id = scheduler.put(activity, password)
        time.sleep(result_ttl.total_seconds())
        young_task_id = scheduler.put(activity, password)
        time.sleep(result_ttl.total_seconds() * 1.5)

        with pytest.raises(TaskIdNotFound):
            scheduler.get(old_task_id)

        assert scheduler.get(young_task_id).data


class Client(threading.Thread):
    def __init__(self, scheduler: Scheduler, tasks: typing.Iterable[typing.Tuple[bytes, str]], result_handler: list):
        super().__init__(daemon=True)
        self._tasks = tasks
        self._scheduler = scheduler
        self._result_handler = result_handler

    def run(self):
        completed_tasks = list()
        running_tasks = [self._scheduler.put(activity, password) for activity, password in self._tasks]
        tasks_num = len(running_tasks)
        while len(completed_tasks) != tasks_num:
            time.sleep(1)
            for task_id in running_tasks:
                try:
                    result = self._scheduler.get(task_id)
                except TaskNotCompleted:
                    pass
                else:
                    completed_tasks.append(result)
                    running_tasks.remove(task_id)

        self._result_handler.extend(completed_tasks)


def test_thread_safe(launch_engine):
    tasks = [
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'),
        (read_file_binary(os.path.join(TEST_DATA, 'without_password.pka')), None),
    ]
    clients_num = WORKERS_NUM * 2
    results = list()
    clients = [Client(launch_engine, tasks, results) for i in range(clients_num)]
    for client in clients:
        client.start()
    for client in clients:
        client.join()

    assert len(results) == len(clients) * len(tasks)


def test_pt_session_restart():
    activity, password = read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123'
    queue_size = 20
    tasks_before_session_restart = queue_size // 2
    tasks_num = tasks_before_session_restart + 1
    workers_num = 1

    with Scheduler(
            queue_size,
            workers_num,
            READ_FILE_TIMEOUT,
            USE_VIRTUAL_DISPLAY,
            RESULT_TTL,
            tasks_before_session_restart
    ) as scheduler:
        running_tasks = [scheduler.put(activity, password) for i in range(tasks_num)]
        while len(running_tasks):
            time.sleep(1)
            for task_id in running_tasks:
                try:
                    result = scheduler.get(task_id)
                except TaskNotCompleted:
                    pass
                else:
                    running_tasks.remove(task_id)
                    assert not result.error


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
def test_net_stabilization_delay(launch_engine, activity, password, net_stabilization_delay, total_percentage):
    task_id = launch_engine.put(activity, password, net_stabilization_delay)
    activity_data = None
    while not activity_data:
        time.sleep(0.5)
        try:
            activity_data = launch_engine.get(task_id)
        except TaskNotCompleted:
            pass
    assert abs(activity_data.data['totalPercentage'] - total_percentage) < 0.5
