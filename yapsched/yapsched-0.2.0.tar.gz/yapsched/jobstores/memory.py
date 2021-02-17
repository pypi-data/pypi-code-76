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

from typing import Optional, List, Dict
import datetime
import re
from . import JobStore, JobAlreadyExistsException, JobDoesNotExistException
from ..job import Job


class MemoryJobStore(JobStore):
    def __init__(self):
        super().__init__()
        self._jobs: List[Job] = []
        self._jobs_map: Dict[str, int] = {}  # job_id -> index

    def teardown(self):
        super().teardown()
        self.remove_all_jobs()

    def add_job(self, job: Job, replace_existing: bool):
        if self.contains_job(job.id):
            if not replace_existing:
                raise JobAlreadyExistsException(job.id)

            self.update_job(job)
            return

        if job.next_run_time is None and job.active:
            job.next_run_time = job.trigger.get_next_fire_time(None, None)

        self._logger.debug(f'Add job ({job}) next run time: {job.next_run_time}')

        index = self._get_job_index(job.next_run_time)

        self._jobs.insert(index, job)
        self._jobs_map[job.id] = index

    def update_job(self, job: Job):
        old_index = self._jobs_map.get(job.id, None)
        if old_index is None:
            raise JobDoesNotExistException(job.id)

        self._logger.debug(f'Update job ({job}) next run time: {job.next_run_time}')

        old_job = self._jobs[old_index]

        if old_job.next_run_time == job.next_run_time:
            self._jobs[old_index] = job
        else:
            del self._jobs[old_index]
            del self._jobs_map[job.id]
            self.add_job(job, False)

    def remove_job(self, job_id: str):
        index = self._jobs_map.get(job_id, None)
        if index is None:
            raise JobDoesNotExistException(job_id)

        self._logger.debug(f'Delete job ({self._jobs[index]})')

        del self._jobs[index]
        del self._jobs_map[job_id]

    def remove_all_jobs(self):
        self._jobs = []
        self._jobs_map = {}

    def get_job(self, job_id: str) -> Job:
        index = self._jobs_map.get(job_id, None)
        if index is None:
            raise JobDoesNotExistException(job_id)
        return self._jobs[index]

    def get_jobs(self, pattern: str = None) -> List[Job]:
        if pattern is None:
            return self._jobs

        return [job for job in self._jobs if re.fullmatch(pattern, job.id)]

    def contains_job(self, job_id: str) -> bool:
        return job_id in self._jobs_map

    def _get_job_index(self, dt: Optional[datetime.datetime]) -> int:
        index = -1

        if dt is not None:
            for i, job in enumerate(self._jobs):
                if dt < job.next_run_time:
                    index = i
                    break

        if index == -1:
            index = len(self._jobs)

        return index

    def _get_stored_instance_id(self) -> int:
        return 0

    def _save_instance_id(self, instance_id: int):
        pass
