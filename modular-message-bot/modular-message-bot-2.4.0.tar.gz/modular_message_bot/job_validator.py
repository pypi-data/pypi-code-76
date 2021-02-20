from typing import List

from modular_message_bot.handlers.abstract_handler import AbstractHandler
from modular_message_bot.handlers.handler_collections import (
    AbstractHandlerCollection,
    InputHandlerCollection,
    OutputHandlerCollection,
    PreHandlerCollection,
    ProcessorHandlerCollection,
)
from modular_message_bot.models.job import JobConfigSection, JobsCollection


class JobValidator(object):
    def __init__(
        self,
        pre_handlers: PreHandlerCollection,
        input_handlers: InputHandlerCollection,
        processor_handlers: ProcessorHandlerCollection,
        output_handlers: OutputHandlerCollection,
    ):
        self.pre_handlers = pre_handlers
        self.input_handlers = input_handlers
        self.processor_handlers = processor_handlers
        self.output_handlers = output_handlers

    def validate(self, jobs: JobsCollection):
        jobs_list = jobs.get_all()

        validation_results = [
            self.validate_handlers("pre", jobs_list),
            self.validate_handlers("input", jobs_list),
            self.validate_handlers("processor", jobs_list),
            self.validate_handlers("output", jobs_list),
        ]
        for validation_result in validation_results:
            if validation_result != "":
                return validation_result
        return ""

    def validate_handlers(self, attr: str, jobs: list):
        job_attribute = f"{attr}s"
        handlers_attribute = f"{attr}_handlers"
        handlers: AbstractHandlerCollection = getattr(self, handlers_attribute)

        # Extract the in-use handlers
        handler_codes: List[str] = []
        for job in jobs:
            job_config: JobConfigSection
            for job_config in getattr(job, job_attribute):
                if job_config.code not in handler_codes:
                    handler_codes.append(job_config.code)

        # Validate each job
        for job in jobs:
            validate_job_config: JobConfigSection
            for validate_job_config in getattr(job, job_attribute):
                handler: AbstractHandler = handlers.get_by_code(validate_job_config.code)
                result = handler.validate_job_config(validate_job_config)
                if result != "":
                    return result

        # No Validation errors
        return ""
