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

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List
from ..util import get_class_logger
from ..job import Job

MIN_INSTANCE_ID = 10000
MAX_INSTANCE_ID = 99999


class JobStore(ABC):
    def __init__(self):
        self._logger = get_class_logger(self)
        self._scheduler = None

        self.last_instance_id: int = 0

    def setup(self):
        pass

    def teardown(self):
        pass

    def get_due_jobs(self, latest: datetime) -> List[Job]:
        jobs = self.get_jobs()
        pending = list(filter(lambda job: job.active and job.next_run_time <= latest, jobs))
        return pending

    def get_next_run_time(self) -> Optional[datetime]:
        jobs = self.get_jobs()
        return jobs[0].next_run_time if jobs else None

    @abstractmethod
    def add_job(self, job: Job, replace_existing: bool):
        pass

    @abstractmethod
    def update_job(self, job: Job):
        pass

    @abstractmethod
    def remove_job(self, job_id: str):
        pass

    @abstractmethod
    def remove_all_jobs(self):
        pass

    @abstractmethod
    def get_job(self, job_id: str) -> Job:
        pass

    @abstractmethod
    def get_jobs(self, pattern: str = None) -> List[Job]:
        pass

    @abstractmethod
    def contains_job(self, job_id: str) -> bool:
        pass

    def get_new_instance_id(self) -> int:
        if self.last_instance_id == 0:
            self._logger.debug('first time generating a new instance ID. getting last one from jobstore')
            self.last_instance_id = self._get_stored_instance_id()
            if self.last_instance_id == 0:
                self._logger.debug(f'no last instance ID in jobstore. using minimum value ({MIN_INSTANCE_ID})')
                # we use MIN - 1 here because of the increment a few lines down
                self.last_instance_id = MIN_INSTANCE_ID - 1
            else:
                self._logger.debug(f'got last instance ID from jobstore ({self.last_instance_id})')

        if self.last_instance_id < MIN_INSTANCE_ID - 1 or self.last_instance_id > MAX_INSTANCE_ID:
            self._logger.error(f'Last instance ID ({self.last_instance_id}) was out of acceptable range '
                               f'([{MIN_INSTANCE_ID}, {MAX_INSTANCE_ID}])! Resetting to minimum value '
                               f'({MIN_INSTANCE_ID})')

            # we use MIN - 1 here because of the increment in the next line of code
            self.last_instance_id = MIN_INSTANCE_ID - 1

        self.last_instance_id += 1

        if self.last_instance_id > MAX_INSTANCE_ID:
            self._logger.debug(f'new instance ID at max ({MAX_INSTANCE_ID}), resetting to min ({MIN_INSTANCE_ID})')
            self.last_instance_id = MIN_INSTANCE_ID

        self._save_instance_id(self.last_instance_id)

        self._logger.debug(f'generated a new instance ID ({self.last_instance_id})')

        return self.last_instance_id

    @abstractmethod
    def _get_stored_instance_id(self) -> int:
        pass

    @abstractmethod
    def _save_instance_id(self, instance_id: int):
        pass


class JobAlreadyExistsException(Exception):
    def __init__(self, job_id):
        super().__init__(f'Job "{job_id}" already exists')


class JobDoesNotExistException(Exception):
    def __init__(self, job_id):
        super().__init__(f'Job "{job_id}" does not exist')
