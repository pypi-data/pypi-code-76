from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Set

from aiohttp import web


@dataclass
class Job:
    func: Callable
    params: Dict[Any, Any]

    def __hash__(self):
        return hash(self.func)


@dataclass
class AbstractExecutor(ABC):
    jobs: Set[Job] = field(default_factory=set, init=False)

    def register(self, **params):
        def wrapper(func: Callable):
            self.jobs.add(Job(func, params))
            return func

        return wrapper

    async def start(self, app: web.Application):
        for job in self.jobs:
            await self.execute(app, job)

    @abstractmethod
    async def execute(self, app: web.Application, job: Job):
        ...

    @abstractmethod
    async def stop(self, app: web.Application):
        ...
