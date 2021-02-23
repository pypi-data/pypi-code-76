import asyncio
from dataclasses import dataclass, field
from typing import Set

from aiohttp import web
from aiocron import crontab, Cron
from croniter import croniter

from simio.app.config_names import AppConfig
from simio.exceptions import InvalidCronFormat
from simio.job.abstract import AbstractExecutor, Job


@dataclass
class AsyncCron(AbstractExecutor):
    _running_tasks: Set[Cron] = field(default_factory=set, init=False)

    async def execute(self, app: web.Application, job: Job):
        cron = job.params.get("cron")

        if not croniter.is_valid(cron):
            raise InvalidCronFormat(f"Cron {cron} has invalid format")

        timezone = app["config"][AppConfig][AppConfig.timezone]

        cron_job = crontab(cron, job.func, args=(app,), tz=timezone)
        self._running_tasks.add(cron_job)

    async def stop(self, app: web.Application):
        tasks = []

        for cron in self._running_tasks:
            tasks.append(self._stop_task(cron))

        await asyncio.gather(*tasks)

    async def _stop_task(self, task: Cron):
        task.stop()
        self._running_tasks.discard(task)
