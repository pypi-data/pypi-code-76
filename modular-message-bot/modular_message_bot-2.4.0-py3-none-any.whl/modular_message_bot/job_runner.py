import logging

from modular_message_bot.config.config_interpolator import ConfigInterpolator
from modular_message_bot.handlers.handler_collections import (
    InputHandlerCollection,
    OutputHandlerCollection,
    PreHandlerCollection,
    ProcessorHandlerCollection,
)
from modular_message_bot.models.job import Job
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection
from modular_message_bot.string_interpolator import StringInterpolator

logger = logging.getLogger(__name__)


class JobRunner(object):
    def __init__(
        self,
        dynamic_config_interpolator: ConfigInterpolator,
        job_string_interpolator: StringInterpolator,
        pre_handlers: PreHandlerCollection,
        input_handlers: InputHandlerCollection,
        processor_handlers: ProcessorHandlerCollection,
        output_handlers: OutputHandlerCollection,
    ):
        self.dynamic_config_interpolator = dynamic_config_interpolator
        self.job_string_interpolator = job_string_interpolator
        self.pre_handlers = pre_handlers
        self.input_handlers = input_handlers
        self.processor_handlers = processor_handlers
        self.output_handlers = output_handlers

    def run_job(self, job: Job):
        logger.info(f"Running job '{job.get_name()}'")

        # Strings
        job_run_vars_collection = self.get_job_run_vars_collection(job)

        # Pre
        if not self.pre_handlers.run(job, job_run_vars_collection):
            return

        # Inputs
        self.input_handlers.run(job, job_run_vars_collection)
        validation_result = self.input_handlers.validate_job_vars(job_run_vars_collection)
        if validation_result != "":
            raise Exception(validation_result)

        # Process
        if not self.processor_handlers.process(job, job_run_vars_collection):
            return

        # Output
        self.output_handlers.output(job, job_run_vars_collection)

    def get_job_run_vars_collection(self, job: Job) -> JobRunVarCollection:
        job_run_vars = JobRunVarCollection(self.job_string_interpolator)
        for key, value in job.vars.items():
            if isinstance(value, str):
                value = self.dynamic_config_interpolator.interpolate(value)
            job_run_vars.add_job_run_var(JobRunVar(key, value, []))
        return job_run_vars
