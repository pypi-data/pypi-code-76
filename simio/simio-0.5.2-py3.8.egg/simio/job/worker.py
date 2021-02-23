import asyncio
from asyncio import Task
from dataclasses import dataclass, field
from typing import Awaitable, Set

from aiohttp import web

from simio.exceptions import WorkerTypeError
from simio.job.abstract import AbstractExecutor, Job


@dataclass
class AsyncWorker(AbstractExecutor):
    _running_tasks: Set[Task] = field(default_factory=set, init=False)

    async def execute(self, app: web.Application, job: Job):
        worker = job.func(app=app)

        if not isinstance(  # pylint: disable=isinstance-second-argument-not-valid-type
            worker, Awaitable,
        ):
            raise WorkerTypeError("You are trying to create worker that is not async!")

        task = asyncio.create_task(worker)
        self._running_tasks.add(task)

    async def stop(self, app: web.Application):
        tasks = []

        for task in self._running_tasks:
            tasks.append(self._stop_task(task))

        await asyncio.gather(*tasks)

    async def _stop_task(self, task: Task):
        task.cancel()
        await task
        self._running_tasks.discard(task)
