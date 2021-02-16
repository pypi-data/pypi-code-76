import threading
import time
import datetime
from thompcoutils.log_utils import get_logger

_time_format = '%H:%M:%S'


class ThreadManager (threading.Thread):
    THREAD_LOCK = threading.Lock()
    threads = {}

    def __init__(self, name, function, *argv):
        threading.Thread.__init__(self)
        self.name = name
        self.function = function
        self.args = argv
        self.rtn = None
        ThreadManager.threads[name] = self

    def run(self):
        self.rtn = self.function(*self.args)

    @staticmethod
    def start_thread(thread_name):
        ThreadManager.threads[thread_name].start_flashing()

    @staticmethod
    def start_all_threads():
        for thread_name in ThreadManager.threads:
            ThreadManager.threads[thread_name].start()

    @staticmethod
    def join_all_threads():
        for thread_name in ThreadManager.threads:
            ThreadManager.threads[thread_name].join()

    @staticmethod
    def join_thread(thread_name):
        ThreadManager.threads[thread_name].join()


class WorkerLoopThread(threading.Thread):
    def __init__(self, callback_function, parameters=None):
        super(WorkerLoopThread, self).__init__()
        logger = get_logger()
        logger.debug("creating a WorkerLoopThread")
        self.function = callback_function
        self.parameters = parameters
        self._is_running = False

    def is_running(self):
        return self._is_running

    def stop(self):
        self._is_running = False

    def start(self):
        if not self._is_running:
            self._is_running = True
            threading.Thread.start(self)

    def run(self):
        logger = get_logger()
        logger.debug("starting WorkerThread")
        while self._is_running:
            if self.parameters is None:
                logger.debug("calling function {}()".format(self.function))
                self.function()
            else:
                logger.debug("calling function {}({})".format(self.function, self.parameters))
                self.function(self.parameters)


class WorkerThread(threading.Thread):
    def __init__(self, callback_function, parameters=None):
        super(WorkerThread, self).__init__()
        logger = get_logger()
        logger.debug("creating a WorkerThread")
        self.function = callback_function
        self.parameters = parameters

    def run(self):
        logger = get_logger()
        logger.debug("starting WorkerThread")
        if self.parameters is None:
            logger.debug("calling function {}()".format(self.function))
            self.function()
        else:
            logger.debug("calling function {}({})".format(self.function, self.parameters))
            self.function(self.parameters)


class Watchdog(threading.Thread):
    def __init__(self, check_period, timeout_function):
        super(Watchdog, self).__init__()
        self.last_tickle = None
        self.is_running = False
        self.check_period = check_period
        self.timeout_function = timeout_function

    def tickle(self):
        self.last_tickle = datetime.datetime.now()

    def stop(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            time.sleep(self.check_period)
            now = datetime.datetime.now()
            time_diff = now - self.last_tickle
            if time_diff.seconds > self.check_period:
                self.timeout_function(self)
