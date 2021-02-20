from abc import abstractmethod

from modular_message_bot.handlers.abstract_handler import AbstractHandler
from modular_message_bot.models.job_run import JobRunVarCollection


class AbstractProcessorHandler(AbstractHandler):
    @abstractmethod
    def process(self, parameters: dict, job_run_vars_collection: JobRunVarCollection) -> bool:
        raise NotImplementedError
