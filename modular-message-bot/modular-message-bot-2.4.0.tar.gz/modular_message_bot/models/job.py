from dataclasses import dataclass
from typing import List

from modular_message_bot.config.config_collection import ConfigCollection
from modular_message_bot.config.constants import SCHEDULER_TIMEZONE_CFG_KEY


@dataclass
class Job(object):
    config: ConfigCollection
    id: str
    schedules: list
    schedules_timezone: str
    vars: dict
    pres: list
    inputs: list
    processors: list
    outputs: list

    def get_name(self):
        if self.id == "":
            return "Unknown"
        return self.id

    def get_schedules_timezone(self) -> str:
        if self.schedules_timezone != "":
            return self.schedules_timezone
        return self.config.get(SCHEDULER_TIMEZONE_CFG_KEY)


@dataclass
class JobConfigSection(object):
    code: str
    parameters: dict


class JobPre(JobConfigSection):
    pass


class JobInput(JobConfigSection):
    pass


class JobProcessor(JobConfigSection):
    pass


class JobOutput(JobConfigSection):
    pass


class JobsCollection(object):
    def __init__(self):
        self.jobs_by_id = {}

    def add_job(self, job: Job):
        if job.id in self.jobs_by_id.keys():
            raise Exception(f"Job id '{job.id}' already exists, check your config for duplicate job ids")
        self.jobs_by_id[job.id] = job

    def get_all(self) -> List[str]:
        return list(self.jobs_by_id.values())

    def get_by_id(self, identifier: str) -> Job:
        if identifier not in self.jobs_by_id.keys():
            raise Exception(f"Job id of '{identifier}' is not found")
        return self.jobs_by_id[identifier]
