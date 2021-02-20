from abc import ABC, abstractmethod

from modular_message_bot.handlers.abstract_handler import AbstractHandler
from modular_message_bot.models.job_run import JobRunVarCollection


class AbstractPreHandler(AbstractHandler, ABC):
    @abstractmethod
    def run(self, parameters: dict, job_run_vars_collection: JobRunVarCollection) -> bool:
        raise NotImplementedError
