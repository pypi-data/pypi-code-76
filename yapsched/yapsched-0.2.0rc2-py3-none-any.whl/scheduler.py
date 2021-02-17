# Copyright 2020 Software Factory Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum, auto
from typing import Optional, Callable, List, Dict
import threading
import uuid
from datetime import datetime, timezone, timedelta
import logging
from .job import Job
from . import executor, jobstores, triggers, events

logger = logging.getLogger(__name__)


class State(Enum):
    STOPPED = auto()
    RUNNING = auto()
    PAUSED = auto()


class Scheduler:
    _event: Optional[threading.Event] = None
    _thread: Optional[threading.Thread] = None

    def __init__(self, pool_size: int = 10, jobstore: Optional[jobstores.JobStore] = None, tz=timezone.utc):
        if tz is None:
            raise ValueError('tz must not be None')

        self._executor = executor.Executor(pool_size, self)
        self._executor_lock = threading.RLock()

        self._jobstore = None
        self._jobstore_lock = threading.RLock()

        self._listeners = []
        self._listeners_lock = threading.RLock()

        self.state = State.STOPPED
        self._instances = {}

        self.tz = None

        self.configure(jobstore=jobstore, tz=tz)

    def configure(self, jobstore: Optional[jobstores.JobStore] = None, tz=None):
        if jobstore is not None:
            jobstore._scheduler = self
        self._jobstore = jobstore

        if tz is not None:
            self.tz = tz

    def start(self, paused: bool = False):
        if self.state != State.STOPPED:
            raise SchedulerAlreadyRunningException

        self._event = threading.Event()

        with self._executor_lock:
            self._executor.setup()

        with self._jobstore_lock:
            self._jobstore.setup()

        self.add_listener(self._internal_listener)

        self.state = State.PAUSED if paused else State.RUNNING
        logger.info('Scheduler started')
        self._dispatch_event(events.SchedulerEvent(events.EVENT_SCHEDULER_STARTED))

        if not paused:
            self.wakeup()

        self._thread = threading.Thread(target=self._main_loop, name='yapsched', daemon=True)
        self._thread.start()

    def shutdown(self, wait: bool = True):
        if self.state == State.STOPPED:
            raise SchedulerNotRunningException

        logger.info('Shutting down...')

        self.state = State.STOPPED

        logger.debug('Closing thread')
        self._event.set()
        self._thread.join()

        logger.debug('Deleting thread')
        del self._thread

        logger.debug('Tearing down executor')
        with self._executor_lock:
            self._executor.teardown(wait)

        logger.debug('Tearing down jobstore')
        with self._jobstore_lock:
            self._jobstore.teardown()

        self._dispatch_event(events.SchedulerEvent(events.EVENT_SCHEDULER_STOPPED))

        self.remove_listener(self._internal_listener)

        logger.info('Scheduler shutdown')

    def pause(self):
        if self.state == State.STOPPED:
            raise SchedulerNotRunningException
        elif self.state == State.RUNNING:
            self.state = State.PAUSED
            logger.info('Scheduler paused')
            self._dispatch_event(events.SchedulerEvent(events.EVENT_SCHEDULER_PAUSED))

    def resume(self):
        if self.state == State.STOPPED:
            raise SchedulerNotRunningException
        elif self.state == State.PAUSED:
            self.state = State.RUNNING
            logger.info('Scheduler resumed')
            self._dispatch_event(events.SchedulerEvent(events.EVENT_SCHEDULER_RESUMED))
            self.wakeup()

    @property
    def running(self) -> bool:
        return self.state != State.STOPPED

    def wakeup(self):
        self._event.set()

    def add_job(self,
                func: Callable,
                args: Optional[List] = None,
                kwargs: Optional[Dict] = None,
                dynamic_args: Optional[Dict[str, Callable]] = None,
                identifier: Optional[str] = None,
                description: Optional[str] = None,
                coalesce: bool = False,
                max_instances: int = -1,
                replace_existing: bool = False,
                trigger: Optional[triggers.Trigger] = None,
                next_run_time: Optional[datetime] = None,
                active: bool = True,
                callback: Optional[Callable] = None,
                error_callback: Optional[Callable] = None) -> Job:
        if next_run_time is not None and not active:
            raise ValueError('Job can\'t be inactive and have a non-null next_run_time!')

        if identifier is None:
            identifier = uuid.uuid4()

        if trigger is None:
            trigger = triggers.DateTrigger(datetime.now(tz=self.tz))

        trigger.tz = self.tz

        job = Job(func,
                  identifier,
                  tuple(args) if args is not None else (),
                  kwargs if kwargs is not None else {},
                  dynamic_args if dynamic_args is not None else {},
                  trigger,
                  next_run_time=next_run_time,
                  description=description,
                  coalesce=coalesce,
                  max_instances=max_instances,
                  active=active,
                  callback=callback,
                  error_callback=error_callback)

        with self._jobstore_lock:
            self._jobstore.add_job(job, replace_existing)

        logger.info(f'Added job {identifier}')
        self._dispatch_event(events.JobEvent(events.EVENT_JOB_ADDED, identifier))

        if self.state == State.RUNNING and active:
            self.wakeup()

        return job

    def modify_job(self, job_id: str, **changes) -> Job:
        with self._jobstore_lock:
            job = self.get_job(job_id)

            new_next_run_time = changes['next_run_time'] if 'next_run_time' in changes else job.next_run_time
            new_active = changes['active'] if 'active' in changes else job.active

            if new_next_run_time is not None and not new_active:
                raise ValueError('Job can\'t be inactive and have a non-null next_run_time!')

            job._modify(**changes)

            if job.trigger is None:
                job.trigger = triggers.DateTrigger(datetime.now(tz=self.tz))

            job.trigger.tz = self.tz

            self._jobstore.update_job(job)

        self._dispatch_event(events.JobEvent(events.EVENT_JOB_MODIFIED, job_id))

        if self.state == State.RUNNING:
            self.wakeup()

        return job

    def get_job(self, job_id: str) -> Job:
        with self._jobstore_lock:
            return self._jobstore.get_job(job_id)

    def get_jobs(self, pattern: str = None) -> List[Job]:
        with self._jobstore_lock:
            return self._jobstore.get_jobs(pattern)

    def remove_job(self, job_id: str):
        with self._jobstore_lock:
            self._jobstore.remove_job(job_id)

        logger.info(f'Removed job {job_id}')
        self._dispatch_event(events.JobEvent(events.EVENT_JOB_REMOVED, job_id))

    def terminate_job(self, instance_id: int):
        with self._executor_lock:
            job_id = self._executor.terminate_job(instance_id)
            logger.info(f'Terminated job {job_id}')
            self._dispatch_event(events.JobEvent(events.EVENT_JOB_TERMINATED, job_id))

    def trigger_job(self, job_id: str) -> int:
        job = self.get_job(job_id)
        run_time = datetime.now(tz=self.tz)

        try:
            instance_id = self._executor.submit_job(job, run_time)
        except executor.MaxJobInstancesReachedException:
            self._dispatch_event(events.JobEvent(events.EVENT_JOB_MAX_INSTANCES, job_id))
            raise

        return instance_id

    def get_job_instance_ids(self, job_id: str) -> List[int]:
        with self._jobstore_lock:
            if not self._jobstore.contains_job(job_id):
                raise jobstores.JobDoesNotExistException(job_id)

        with self._executor_lock:
            return self._executor.get_job_instance_ids(job_id)

    def get_job_with_instance_id(self, instance_id: int) -> Job:
        with self._executor_lock:
            return self._executor.get_job(instance_id)

    def get_running_jobs(self) -> List[dict]:
        with self._executor_lock:
            return self._executor.get_instances()

    def add_listener(self, callback: Callable, mask: int = events.EVENT_ALL):
        with self._listeners_lock:
            self._listeners.append((callback, mask))

    def remove_listener(self, callback):
        with self._listeners_lock:
            for i, (cb, _) in enumerate(self._listeners):
                if callback == cb:
                    del self._listeners[i]

    def _main_loop(self):
        max_wait = threading.TIMEOUT_MAX
        wait_seconds = max_wait
        while self.state != State.STOPPED:
            self._event.wait(wait_seconds)
            self._event.clear()
            if self.state == State.STOPPED:
                break
            wait_seconds = self._process_jobs()
            if wait_seconds == -1:
                wait_seconds = max_wait

    def _process_jobs(self) -> int:
        if self.state == State.PAUSED:
            logger.debug('Scheduler paused; not processing jobs')
            return -1

        logger.debug('Processing jobs')
        now_dt = datetime.now(tz=self.tz)
        next_wakeup_time: Optional[datetime] = None
        events_to_dispatch = []

        with self._jobstore_lock:
            try:
                due_jobs = self._jobstore.get_due_jobs(now_dt)
                logger.debug(f'Due jobs: {due_jobs}')

                for job in due_jobs:
                    run_times = job._get_run_times(now_dt)
                    run_times = run_times[-1:] if job.coalesce else run_times
                    logger.debug(f'Job: {job}; run times: {run_times}')

                    for run_time in run_times:
                        try:
                            self._executor.submit_job(job, run_time)
                        except executor.MaxJobInstancesReachedException as e:
                            logger.error(f'Execution of job skipped: {e}')
                            events_to_dispatch.append(events.JobEvent(events.EVENT_JOB_MAX_INSTANCES, job.id))
                        except Exception as e:
                            logger.exception(e)
                        else:
                            events_to_dispatch.append(events.JobEvent(events.EVENT_JOB_SUBMITTED, job.id))

                    job_next_run_time = job.trigger.get_next_fire_time(run_times[-1], None)
                    logger.debug(f'Job next run time: {job_next_run_time}')
                    if job_next_run_time:
                        job.next_run_time = job_next_run_time
                        self._jobstore.update_job(job)
                    else:
                        self.remove_job(job.id)
            except Exception as e:
                logger.warning(f'Error getting due jobs from job store: {e}')
                next_wakeup_time = now_dt + timedelta(seconds=5)

            jobstore_next_run_time = self._jobstore.get_next_run_time()
            logger.debug(f'Jobstore next run time: {jobstore_next_run_time}')
            if jobstore_next_run_time is not None and next_wakeup_time is None:
                next_wakeup_time = jobstore_next_run_time

        for event in events_to_dispatch:
            self._dispatch_event(event)

        if self.state == State.PAUSED:
            wait_seconds = -1
            logger.debug('Scheduler is paused; waiting for resume')
        elif next_wakeup_time is None:
            wait_seconds = -1
            logger.debug('No jobs; waiting until a job is added')
        else:
            wait_seconds = min(max((next_wakeup_time - now_dt).total_seconds(), 0), int(threading.TIMEOUT_MAX))
            logger.debug(f'Next wakeup is due at {next_wakeup_time} (in {wait_seconds} seconds)')

        return wait_seconds

    def _dispatch_event(self, event: events.Event):
        with self._listeners_lock:
            listeners = tuple(self._listeners)

        for callback, mask in listeners:
            if event.code & mask:
                try:
                    callback(event)
                except Exception as e:
                    logger.error('Error notifying listener')
                    logger.exception(e)

    def _internal_listener(self, event: events.Event):
        if isinstance(event, events.JobExecutionEvent):
            if event.code == events.EVENT_JOB_EXECUTED:
                with self._jobstore_lock:
                    logger.info(f'Next wakeup time: {self._jobstore.get_next_run_time()}')


class SchedulerAlreadyRunningException(Exception):
    def __init__(self):
        super().__init__('Scheduler is already running')


class SchedulerNotRunningException(Exception):
    def __init__(self):
        super().__init__('Scheduler is not running')


class JobAlreadyExistsException(Exception):
    def __init__(self, job_id: str):
        super().__init__(f'Job already exists with ID {job_id}')
        self.job_id = job_id
