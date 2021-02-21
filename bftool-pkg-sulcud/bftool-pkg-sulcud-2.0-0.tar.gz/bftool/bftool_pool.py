import asyncio
import collections
import concurrent.futures
import multiprocessing
import multiprocessing.pool
import queue
import sys
import threading
import time

from .arguments import Arguments

__all__ = ["Pool"]


class Queue(object):
    def __init__(self, values):
        self.__reference = values
        self._values = multiprocessing.Queue()
        self._stop = multiprocessing.Event()
        self._complete = multiprocessing.Event()
        self._thread = threading.Thread(target=self.__fill, )
        self._thread.start()

    def __fill(self):
        for element in self.__reference:
            if self._stop.is_set():
                break
            self._values.put(element)
        self._complete.set()

    def empty(self):
        if self._complete.is_set():
            return self._values.empty()
        return False

    def get(self, block=True, timeout=None):
        return self._values.get(block=block, timeout=timeout)

    def join(self):
        self._thread.join()

    def stop(self):
        self._stop.set()


async def _call_blocking(loop: asyncio.AbstractEventLoop, executor: concurrent.futures.Executor, func, *args):
    futures = [
        loop.run_in_executor(executor, func, *args)]
    while futures:
        done, futures = await asyncio.wait(
            futures,
            loop=loop, return_when=asyncio.ALL_COMPLETED
        )
        for f in done:
            await f
            return f.result()


class Pool(object):
    def __init__(
            self,
            function_: collections.abc.Callable,
            function_arguments: collections.abc.Iterable[collections.abc.Iterable] or Arguments,
            check_function: collections.abc.Callable = lambda _: True,
            success_function: collections.abc.Callable = print,
            max_processes: int = 1,
            max_threads: int = 1,
            optimize_workers: bool = True,
            speed_reference: float = 0.001,  # 1000 operations in 1 second
            processes_as_threads: bool = False,
            unsafe_workers: bool = False
    ):
        if not isinstance(function_, collections.abc.Callable):
            raise ValueError("function_ must be callable")
        if not unsafe_workers:
            if max_threads > 300:
                raise ResourceWarning("Exceeded the safe amount of threads per process (300)")
            elif max_processes > 100:
                raise ResourceWarning("Exceeded the safe amount of processes (100)")
        if max_processes == 0:
            raise ValueError("max_processes can't be zero")
        if max_threads == 0:
            raise ValueError("max_threads can't be zero")
        self._function = function_
        self._check_function = check_function
        self._success_function = success_function
        self._processes = max_processes
        self._threads = max_threads
        self._optimize_workers = optimize_workers
        self._blocking_success = None

        self._processes_as_threads = processes_as_threads
        self.__speed_reference = speed_reference

        self._success_sync_queue = None
        self._running = False
        self._complete = multiprocessing.Event()

        self._raw_function_arguments = (v for v in function_arguments)

        self._start_thread = None
        self._function_arguments = None

    def _sync_success(self):
        while not self._complete.is_set():
            try:
                self._success_function(self._success_sync_queue.get(timeout=0))
            except queue.Empty:
                continue
        while not self._success_sync_queue.empty():
            try:
                self._success_function(self._success_sync_queue.get(timeout=0))
            except queue.Empty:
                continue

    def _get(self):
        return self._function_arguments.get(timeout=0)

    async def _callback(self, loop: asyncio.AbstractEventLoop, executor: concurrent.futures.Executor):
        while not self._function_arguments.empty():
            try:
                args = await _call_blocking(loop, executor, self._get)
            except queue.Empty:
                continue
            output = await _call_blocking(loop, executor, self._function, *args)
            is_valid = await _call_blocking(loop, executor, self._check_function, output)
            if is_valid:
                if self._blocking_success:
                    self._success_function(output)
                else:
                    await _call_blocking(loop, executor, self._success_sync_queue.put, output)

    async def __process_worker(self, loop: asyncio.AbstractEventLoop, executor: concurrent.futures.Executor):
        futures = [self._callback(loop, executor) for _ in range(self._threads)]
        while futures:
            done, futures = await asyncio.wait(
                futures,
                loop=loop,
                return_when=asyncio.ALL_COMPLETED
            )
            for f in done:
                await f

    def _process_worker(self):
        for try_ in range(5):
            try:
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=self._threads)
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.__process_worker(loop, executor))
                loop.close()
                executor.shutdown(wait=True)
                return
            except ImportError:
                pass

    def run(self) -> float:
        if self._complete.is_set():
            raise StopIteration("This runner has already being used")
        if self._running:
            raise StopIteration("This runner is being executed")
        self._running = True
        if (self._threads != 1 or self._processes != 1) and self._optimize_workers:
            t = time.time()
            result = self._function(*next(self._raw_function_arguments))
            time_spent = time.time() - t
            if self._check_function(result):
                self._success_function(result)
            if time_spent < self.__speed_reference:
                self._threads = 1
                self._processes = 1
                self._function_arguments = self._raw_function_arguments
        else:
            self._function_arguments = self._raw_function_arguments

        if self._threads == self._processes and self._threads == 1:
            self._function_arguments: collections.Iterable
            start = time.time()
            for args in self._function_arguments:
                output = self._function(*args)
                if self._check_function(output):
                    self._success_function(output)
            return time.time() - start

        self._function_arguments = Queue(self._raw_function_arguments)
        if self._processes == 1 or self._threads == 1:
            if self._processes > self._threads:
                self._threads = self._processes
            self._blocking_success = True
            start = time.time()
            self._process_worker()
            return time.time() - start
        self._blocking_success = False
        self._success_sync_queue = multiprocessing.Queue()
        sync_thread = threading.Thread(target=self._sync_success, )
        sync_thread.start()
        if any(platform in sys.platform for platform in ("win", "ios")) or self._processes_as_threads:
            process_pool = multiprocessing.pool.ThreadPool
        else:
            process_pool = multiprocessing.pool.Pool
        start = time.time()
        pool = process_pool(processes=self._processes)
        pool.imap_unordered(lambda f: f(), (self._process_worker for _ in range(self._processes)),
                            chunksize=self._processes)
        pool.close()
        pool.join()
        pool.terminate()
        self._complete.set()
        self._function_arguments.stop()
        self._function_arguments.join()
        sync_thread.join()
        self._running = False
        return time.time() - start
