#!/usr/bin/env python

#  Raymond Kirk (Tunstill) Copyright (c) 2020
#  Email: ray.tunstill@gmail.com

# LoadBalancing utilities from raytils (https://github.com/RaymondKirk/raytils, https://pypi.org/project/raytils/)
from typing import Callable, Union, List, Tuple

from raytils.system import available_cpu_count
from raytils.time import FPSCounter

import queue

import threading

from timeit import default_timer as timer


class Worker(threading.Thread):
    """Runs jobs from LoadBalancer.

    Work from the LoadBalancer should be in the form of [func, args, kwargs].
    func should take a parameter job_meta containing specifics about the worker running the job.
    """
    def __init__(self, q: queue.Queue, worker_id: int, *args, **kwargs):
        self.q = q
        self.worker_id = worker_id
        self.data_retrieval_rate = FPSCounter(q.maxsize)
        self.processing_rate = FPSCounter(q.maxsize)
        super(Worker, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            try:
                self.data_retrieval_rate.tic()
                work = self.q.get()
                self.data_retrieval_rate.toc()
            except queue.Empty:
                return

            # Create dictionary of meta values to pass to the worker
            job_meta = {
                "worker_id": self.worker_id,  # This is my id
                "worker_data_retrieval_rate": self.data_retrieval_rate.get_fps(),  # I get data every n times per second
                "worker_job_processing_rate": self.processing_rate.get_fps(),  # I process data every n times per second
            }

            self.processing_rate.tic()
            work[0](*work[1], job_meta=job_meta, **work[2])
            self.processing_rate.toc()
            self.q.task_done()


class LoadBalancer(queue.Queue):
    """Add jobs in the form of (func, args, kwargs) to a task queue and automatically scales number of workers.

    Usage:

    .. code-block:: python

        from raytils.system import LoadBalancer
        # We will add heavy tasks to the worker to not block the main thread
        workers = LoadBalancer(maxsize=30, threads=8)

        # Your function must have a job_meta keyword argument so your workers
        # can pass important information about themselves
        def save_dict(file_path, data, job_meta):
            import json
            with open(file_path, "w") as fh:
                json.dump(data, fh)

        # Save 10000 dictionaries to files to demonstrate a heavy load
        for idx in range(10000):
            dict_to_save = {i: i for i in range(10000)}
            file_path = f"{idx}.json"
            # Serially we would do save_dict(file_path, dict_to_save)
            # However we can do it much faster
            workers.add_task(save_dict, [file_path, dict_to_save])
    """
    def __init__(self, maxsize: int = 0, threads: int = 1, auto: bool = True):
        """
        Example:
        Args:
            maxsize: Maximum size of the created jobs queue. If maxsize is <= 0, the queue size is infinite.
            threads: Number of workers to start threads for
            auto: If true workers will be automatically created if the demand is too high.
        """
        super(LoadBalancer, self).__init__(maxsize=maxsize)
        self.max_threads = available_cpu_count()
        self.auto = auto
        self.number_of_threads = 0
        self.tasks_per_second = FPSCounter(queue_length=maxsize)
        # Number of seconds to allow queue to catch up before adding more cores
        self._thread_grace_period = 2.0  # TODO: these hard-coded values should be tunable
        self._last_thread_added = timer()
        self._add_thread_threshold_percent = 0.8  # TODO: these hard-coded values should be tunable
        for _ in range(threads):
            self._add_thread(check_grace_period=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.join()

    def _add_thread(self, check_grace_period: bool = True):
        """Function that's used internally. If the queue of jobs ever becomes full a new thread is spawned to try to
        handle the new information in realtime"""
        # Do not add more threads if the CPU cannot support it
        if self.number_of_threads >= self.max_threads:
            return

        # Grace period so cores don't quickly accelerate to system maximum
        if check_grace_period and (timer() - self._last_thread_added) <= self._thread_grace_period:
            return

        Worker(self, self.number_of_threads).start()
        self.number_of_threads += 1
        self._last_thread_added = timer()

    def add_task(self, func: Callable, args: Union[List, Tuple] = None, kwargs: dict = None, wait: bool = False):
        """Add a task to be processed by one of the available workers

        Args:
            func: callable of the signature func(*args, **kwargs) or func(arg1, arg2, ..., kwarg1, job_meta=None)
            args: list of arguments to pass to the func calling func(*args, job_meta={...}, **kwargs)
            kwargs: list of keyword arguments to pass to the func calling func(*args, job_meta={...}, **kwargs)
            wait: If true blocks until the item is placed in the queue

        Returns:
            bool: True if item placed in the queue otherwise false
        """
        # If the number of tasks_per_second being added is lower than the current approx queue size
        # then add a thread to deal with the extra work
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.tasks_per_second.toc()
        self.tasks_per_second.tic()

        # Add a thread if queue_size growing faster than current processing or is nearing capacity
        if self.auto:
            queue_size = self.qsize()
            queue_capacity = queue_size / self.maxsize
            if queue_size >= self.tasks_per_second.get_fps() or queue_capacity >= self._add_thread_threshold_percent:
                self._add_thread()

        try:
            if wait:
                self.put((func, args, kwargs))
            else:
                self.put_nowait((func, args, kwargs))
        except queue.Full:
            if self.auto:
                # If the queue becomes full add a thread to balance the workload
                self._add_thread()  # attempt to add a thread to balance the workload
            return False

        return True
