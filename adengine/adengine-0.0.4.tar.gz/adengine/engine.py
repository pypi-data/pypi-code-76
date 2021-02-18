import dataclasses
import multiprocessing as mp
import os
import datetime
import uuid
import tempfile
import signal
import logging
import threading
import time

from .pt import *


logger = logging.getLogger('adengine.engine')


__all__ = [
    'ActivityData',

    'Scheduler',

    'SchedulerError',
    'TaskIdNotFound',
    'TaskNotCompleted',
    'QueueIsFull',
]


@dataclasses.dataclass(frozen=True)
class Task:
    """This class represents the task for Scheduler."""
    id: str = dataclasses.field(init=False, default_factory=lambda: str(uuid.uuid4()))
    activity: bytes
    password: str
    net_stabilization_delay: int


@dataclasses.dataclass(frozen=True)
class ActivityData:
    """This class represents the result of extracting data."""
    error: ExtractorError
    data: dict


class Worker:
    """Worker for extract data in an isolated process.

    All logic is stored in __call__ method. The Worker starts Packet tracer session and blocks until reading the new task
    from the queue after that worker extracts data from the activity file and push the result to the resulting pool.
    If any error occurred while extraction, it is written to the corresponding attribute in ActivityData instance
    and the data attribute is set to None.

    When __call__ executes, it creates a temporary file to write activity binaries to in specified working directory.
    By default, it is strongly recommended to set the temporary directory in your OS as working directory every time,
    except debugging purposes. Temporary directory depends on your OS:
    /tmp in Linux, C:\\Users\\<username>\\AppData\\Local\\Temp in Windows.

    When a process with running Worker terminated, Worker erases temporary file and terminate Packet Tracer process.
    """
    def __init__(self,
                 queue: mp.Queue,
                 result_pool: dict,
                 work_dir: str,
                 _read_file_timeout: int,
                 use_virtual_display=False,
                 tasks_before_session_restart=100):
        """Initialize Worker

        Args:
            queue: Queue to get tasks from.
            result_pool: Result pool to store results after extracting.
            work_dir: Working directory. Strongly recommend to set the temporary directory of your OS, or it's subdirectory.
            _read_file_timeout: Timeout for reading activity file (in seconds).
            use_virtual_display: If set to True, start Packet Tracer with gui in virtual display.
            tasks_before_session_restart: Number of tasks before restarting PacketTracer session.
        """
        self._queue = queue
        self._result_pool = result_pool
        self._work_dir = work_dir
        self._read_file_timeout = _read_file_timeout
        self._use_virtual_display = use_virtual_display
        self._tasks_before_session_restart = tasks_before_session_restart

    def __repr__(self):
        args = (
            self._queue,
            self._result_pool,
            self._work_dir,
            self._read_file_timeout,
            self._use_virtual_display,
            self._tasks_before_session_restart,
        )
        return f'{self.__class__.__name__}({", ".join(obj.__repr__() for obj in args)})'

    def __call__(self, *args, **kwargs):
        """Method with main Worker logic.

        Executes extracting data from activity files.\n
        All arguments provided for this method are ignored.

        Args:
            *args: unused args
            **kwargs: unused kwargs
        """
        logger.debug(f'Starting worker {os.getpid()}')

        signal.signal(signal.SIGTERM, self._stop)

        self._filepath = os.path.join(self._work_dir, f'activity{os.getpid()}.pka')

        task_counter = 0

        self._start_session()

        while True:
            if task_counter == self._tasks_before_session_restart:
                self._stop_session()
                self._start_session()
                task_counter = 0

            task = self._queue.get(True)
            task_counter += 1
            logger.debug(f'Worker {os.getpid()} reserved task {task.id}')

            with open(self._filepath, 'wb') as file:
                file.write(task.activity)

            before = datetime.datetime.now()
            try:
                data = extract_data(self._session,
                                    self._filepath,
                                    task.password,
                                    self._read_file_timeout,
                                    task.net_stabilization_delay)
            except ExtractorError as e:
                error = e
                data = None
            else:
                error = None
            after = datetime.datetime.now()

            self._result_pool[task.id] = ActivityData(error, data), after
            logger.debug(f'Task {task.id} completed. Time consumed: {after - before}')

    def _clean(self):
        """Cleans all temporary files and directories, created during executing."""
        if os.path.exists(self._filepath):
            os.remove(self._filepath)
            logger.debug(f'Worker {os.getpid()} removed temporary file')

    def _stop(self, signum, frame):
        """Stops Worker on capture SIGTERM signal."""
        del signum, frame  # unused
        logger.debug(f'Stop worker {os.getpid()}...')
        try:
            self._stop_session()
            self._clean()
        except Exception as e:
            logger.debug(f'Worker {os.getpid()} stopped with error: {e}')
            exit(1)
        else:
            logger.debug(f'Worker {os.getpid()} stopped correctly')
            exit(0)

    def _stop_session(self):
        """Stops PacketTracer session"""
        if self._session and self._session.running:
            self._session.stop()

    def _start_session(self):
        """Starts new PacketTracer session"""
        self._session = PacketTracerSession(use_virtual_display=self._use_virtual_display)
        self._session.start()


class SchedulerError(Exception):
    """Base Scheduler exception."""
    pass


class TaskIdNotFound(SchedulerError):
    """This exception is thrown when task id not found in result pool or in not completed tasks."""
    pass


class TaskNotCompleted(SchedulerError):
    """This exception is thrown when task with requested task id not completed."""
    pass


class QueueIsFull(SchedulerError):
    """This exception is thrown when user it trying to put new task to Scheduler with full queue."""
    pass


class Scheduler:
    """Class to control Workers.

    This class is used to control Workers. Scheduler lifecycle:
        1. Creates a queue for tasks with max size specified in queue_size.
        2. Creates result pool to store results of extraction.
        3. Creates a pool of workers with the size specified in workers_num.
        4. Creates subdirectory in OS temporary directory.

    On-call start() method, Scheduler start all Workers in the pool in different processes.\n
    On-call stop() method, Scheduler terminates all Workers processes.

    This class can be used as context manager:
        * When enter context - start() method is used.
        * When leave context - stop() method is used.
    """
    def __init__(self,
                 queue_size: int,
                 workers_num: int,
                 read_file_timeout: int,
                 use_virtual_display=False,
                 result_ttl=datetime.timedelta(minutes=5),
                 tasks_before_session_restart=100):
        """Initialize Scheduler.

        Args:
            queue_size: Size of the queue with tasks.
            workers_num: Number of workers.
            use_virtual_display: If set to True, start Packet Tracer with gui in virtual display.
            result_ttl: Time to wait before delete result.
            tasks_before_session_restart: Number of tasks before restarting PacketTracer session.
        """
        self._queue_size = queue_size
        self._queue = mp.Queue(queue_size)
        self._manager = mp.Manager()
        self._result_pool = self._manager.dict()
        self._not_completed_tasks = set()
        self._use_virtual_display = use_virtual_display
        self._result_ttl = result_ttl
        self._tasks_before_restart = tasks_before_session_restart
        self._read_file_timeout = read_file_timeout

        self._working_dir = os.path.join(tempfile.gettempdir(), 'adengine')
        os.makedirs(self._working_dir, exist_ok=True)

        self._workers = [mp.Process(
            name=f'adengine_worker_{i}',
            target=Worker(self._queue,
                          self._result_pool,
                          self._working_dir,
                          self._read_file_timeout,
                          self._use_virtual_display,
                          self._tasks_before_restart)
        ) for i in range(workers_num)]

        self._put_lock = threading.Lock()
        self._get_lock = threading.Lock()

        self._is_alive = False

    def __repr__(self):
        args = (
            self._queue_size,
            len(self._workers),
            self._use_virtual_display,
            self._tasks_before_restart
        )
        return f'{self.__class__.__name__}({", ".join(obj.__repr__() for obj in args)})'

    def start(self):
        logger.debug('Starting scheduler...')
        for _worker in self._workers:
            _worker.start()
        threading.Thread(target=self._clean_result_pool,
                         name='ResultPoolCleaner',
                         daemon=True).start()
        self._is_alive = True

    def stop(self):
        logger.debug('Stop scheduler...')
        for worker in self._workers:
            worker.terminate()
        self._manager.shutdown()
        self._is_alive = False
        logger.debug('Scheduler stopped')

    def put(self, activity: bytes, password: str, net_stabilization_delay=0) -> str:
        """Puts task in queue.

        Puts task instance in queue. If the queue is full, raises QueueIsFull exception.

        Args:
            activity: Binary representation of activity file.
            password: Password for activity.
            net_stabilization_delay: Delay for network stabilization.

        Returns:
            If the task is created correctly, returns task id.

        Raises:
            QueueIsFull: when try to put task in full queue.
        """
        with self._put_lock:
            if self._queue.full():
                logger.debug(f'Queue of Scheduler {os.getpid()} is full')
                raise QueueIsFull()

            task = Task(activity, password, net_stabilization_delay)
            self._queue.put(task)  # blocking safe process operation
            self._not_completed_tasks.add(task.id)
            logger.debug(f'Created task {task.id}')
            return task.id

    def get(self, task_id: str) -> ActivityData:
        """Gets extraction result from result pool.

        Tries to get a task with provided task id from result poll.\n
        If the task is in work, raises TaskInProgress exception.\n
        If the task is not found in result pool and not on progress, it is considered as unknown task and Scheduler raises
        TaskIdNotFound exception.

        Args:
            task_id: Task ID to get.

        Returns:
            An instance of ActivityData for requested task id.

        Raises:
            TaskNotFoundError: when task id not found.
            TaskNotCompleted: when task is not completed yet.
        """
        with self._get_lock:
            if task_id not in self._not_completed_tasks:
                logger.debug(f'Task {task_id} not found')
                raise TaskIdNotFound()
            elif task_id not in self._result_pool:
                logger.debug(f'Task {task_id} not completed')
                raise TaskNotCompleted()
            else:
                self._not_completed_tasks.remove(task_id)
                logger.debug(f'Return task {task_id}')
                return self._result_pool.pop(task_id)[0]

    def _clean_result_pool(self):
        while True:
            logger.debug(f'ResultPoolCleaner sleep for {self._result_ttl}...')
            time.sleep(self._result_ttl.total_seconds())
            logger.debug(f'Start cleaning...')

            if not self._is_alive:
                return

            with self._get_lock:
                results = tuple(self._result_pool.items())

            curr_time = datetime.datetime.now()
            for task_id, (_, finish_time) in results:
                if curr_time - finish_time > self._result_ttl:
                    logger.debug(f'Task {task_id} reached ttl')
                    try:
                        self.get(task_id)
                    except TaskIdNotFound:
                        pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
