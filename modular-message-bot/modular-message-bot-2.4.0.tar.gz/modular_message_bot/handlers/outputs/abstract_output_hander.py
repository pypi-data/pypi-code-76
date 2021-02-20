from abc import ABC, abstractmethod

from modular_message_bot.handlers.abstract_handler import AbstractHandler
from modular_message_bot.models.job_run import JobRunVarCollection


class AbstractOutputHandler(AbstractHandler, ABC):
    @abstractmethod
    def run(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        raise NotImplementedError


class AbstractSimpleOutputHandler(AbstractOutputHandler, ABC):
    def run(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        params_interpolated = self.dynamic_config_interpolator.interpolate_dict(parameters)
        params_with_strings = job_run_vars_collection.interpolate_into_parameters(params_interpolated)
        self.run_output(params_with_strings)

    @abstractmethod
    def run_output(self, parameters: dict):
        raise NotImplementedError
