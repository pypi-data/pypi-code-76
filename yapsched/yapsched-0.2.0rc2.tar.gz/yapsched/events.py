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

from dataclasses import dataclass
from datetime import datetime
from typing import Any
import traceback

EVENT_SCHEDULER_STARTED = 2 ** 0
EVENT_SCHEDULER_STOPPED = 2 ** 1
EVENT_SCHEDULER_PAUSED = 2 ** 2
EVENT_SCHEDULER_RESUMED = 2 ** 3
EVENT_ALL_JOBS_REMOVED = 2 ** 4
EVENT_JOB_ADDED = 2 ** 5
EVENT_JOB_REMOVED = 2 ** 6
EVENT_JOB_MODIFIED = 2 ** 7
EVENT_JOB_EXECUTED = 2 ** 8
EVENT_JOB_ERROR = 2 ** 9
EVENT_JOB_MISSED = 2 ** 10
EVENT_JOB_SUBMITTED = 2 ** 11
EVENT_JOB_MAX_INSTANCES = 2 ** 12
EVENT_JOB_TERMINATED = 2 ** 13

# UPDATE THIS WHENEVER AN EVENT IS ADDED/REMOVED!
# if the last event is 2 ** x, this should be 2 ** (x + 1) - 1
EVENT_ALL = 2 ** 14 - 1


@dataclass
class Event:
    code: int


class SchedulerEvent(Event):
    pass


@dataclass
class JobEvent(Event):
    job_id: str


class JobExecutionEvent(JobEvent):
    def __init__(self, code: int, job_id: str, instance_id: int, run_time: datetime, success: bool, retval: Any = None,
                 exc: Exception = None):
        super().__init__(code, job_id)

        self.instance_id = instance_id
        self.run_time = run_time
        self.success = success
        self.retval = retval
        self.exc = exc

        if self.exc is not None:
            self.formatted_exc = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)).rstrip()
        else:
            self.formatted_exc = None
