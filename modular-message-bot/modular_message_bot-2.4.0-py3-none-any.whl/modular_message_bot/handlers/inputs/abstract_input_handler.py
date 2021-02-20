from abc import ABC, abstractmethod

from modular_message_bot.handlers.abstract_handler import AbstractHandler
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection


class AbstractInputHandler(AbstractHandler, ABC):
    @abstractmethod
    def validate_job_run_var(self, job_run_var: JobRunVar):
        raise NotImplementedError

    @abstractmethod
    def run(self, parameters: dict, job_run_var_collection: JobRunVarCollection):
        raise NotImplementedError


class AbstractSimpleInputHandler(AbstractInputHandler, ABC):
    def validate_job_run_var(self, job_run_var: JobRunVar):
        return ""

    def run(self, parameters: dict, job_run_var_collection: JobRunVarCollection):
        params_interpolated = self.dynamic_config_interpolator.interpolate_dict(parameters)
        params_with_strings = job_run_var_collection.interpolate_into_parameters(params_interpolated)
        self.run_input(params_with_strings, job_run_var_collection)

    @abstractmethod
    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        raise NotImplementedError
