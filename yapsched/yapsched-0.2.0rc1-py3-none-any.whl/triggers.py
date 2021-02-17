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

from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Optional
from croniter import croniter
from .util import get_class_logger


class Trigger(ABC):
    def __init__(self):
        self.logger = get_class_logger(self)
        self.tz = timezone.utc

    @abstractmethod
    def get_next_fire_time(self, previous: Optional[datetime] = None, latest: Optional[datetime] = None) -> Optional[datetime]:
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class DateTrigger(Trigger):
    def __init__(self, run_time: datetime):
        super().__init__()
        self.run_time = run_time

    def get_next_fire_time(self, previous: Optional[datetime] = None, latest: Optional[datetime] = None) -> Optional[datetime]:
        next_fire_time = self.run_time if previous is None or self.run_time > previous else None
        return next_fire_time

    def __getstate__(self):
        return {
            'run_time': self.run_time
        }

    def __setstate__(self, state):
        self.run_time = state['run_time']

    def __repr__(self):
        return f'<{self.__class__.__name__} (run_time="{self.run_time}")>'

    def __str__(self):
        return f'date[{self.run_time}]'


class CronTrigger(Trigger):
    def __init__(self, cron_str: str):
        super().__init__()
        self.cron_str = cron_str

    def get_next_fire_time(self, previous: Optional[datetime] = None, latest: Optional[datetime] = None) -> Optional[datetime]:
        if previous is None:
            previous = datetime.now(tz=self.tz)

        itr = croniter(self.cron_str, previous)

        next_fire_time = datetime.fromtimestamp(itr.get_next(), tz=self.tz)

        if latest is not None and next_fire_time > latest:
            return None

        return next_fire_time

    def __repr__(self):
        return f'<{self.__class__.__name__} (cron_str="{self.cron_str}")>'

    def __str__(self):
        return f'cron[{self.cron_str}]'
