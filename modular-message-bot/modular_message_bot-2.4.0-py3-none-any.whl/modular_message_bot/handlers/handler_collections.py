import logging

from modular_message_bot.handlers.abstract_handler import AbstractHandler
from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractInputHandler
from modular_message_bot.handlers.outputs.abstract_output_hander import AbstractOutputHandler
from modular_message_bot.handlers.pres.abstract_pre_handler import AbstractPreHandler
from modular_message_bot.handlers.processors.abstract_processor_handler import AbstractProcessorHandler
from modular_message_bot.models.job import Job, JobInput, JobOutput, JobPre, JobProcessor
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection

logger = logging.getLogger(__name__)


class AbstractHandlerCollection(object):
    def __init__(self):
        self.handlers_by_code = {}

    def add_handlers(self, handlers: list):
        for handler in handlers:
            self.add_handler(handler)

    def add_handler(self, handler: AbstractHandler):
        if handler.get_code() in self.handlers_by_code.keys():
            raise Exception(f"Error: '{handler.get_code()}' already present")
        self.handlers_by_code[handler.get_code()] = handler

    def get_by_code(self, code: str) -> AbstractHandler:
        if code not in self.handlers_by_code.keys():
            raise Exception(f"Error: '{code}' not found, please check your jobs config")
        return self.handlers_by_code[code]

    def get_all(self) -> list:
        return list(self.handlers_by_code.values())


class PreHandlerCollection(AbstractHandlerCollection):
    def run(self, job: Job, job_run_vars_collection: JobRunVarCollection) -> bool:
        job_pre: JobPre
        for job_pre in job.pres:
            pre_handler: AbstractHandler = self.get_by_code(job_pre.code)
            if isinstance(pre_handler, AbstractPreHandler):
                result = pre_handler.run(job_pre.parameters, job_run_vars_collection)
                if not result:
                    logger.info(f"Job pre '{job_pre.code}' aborted the job")
                    return False
        return True


class InputHandlerCollection(AbstractHandlerCollection):
    def run(self, job: Job, run_strings_collection: JobRunVarCollection):
        job_input: JobInput
        for job_input in job.inputs:
            input_handler: AbstractHandler = self.get_by_code(job_input.code)
            if isinstance(input_handler, AbstractInputHandler):
                input_handler.run(job_input.parameters, run_strings_collection)

    def validate_job_vars(self, job_run_vars_collection: JobRunVarCollection):
        job_run_var: JobRunVar
        for job_run_var in job_run_vars_collection.get_all():
            for input_code in job_run_var.interpolated_by_input_codes:
                input_handler: AbstractHandler = self.get_by_code(input_code)
                if isinstance(input_handler, AbstractInputHandler):
                    validation_result = input_handler.validate_job_run_var(job_run_var)
                    if validation_result != "":
                        return validation_result
        return ""


class ProcessorHandlerCollection(AbstractHandlerCollection):
    def process(self, job: Job, run_strings_collection: JobRunVarCollection) -> bool:
        job_processor: JobProcessor
        for job_processor in job.processors:
            processor_handler: AbstractHandler = self.get_by_code(job_processor.code)
            if isinstance(processor_handler, AbstractProcessorHandler):
                result = processor_handler.process(job_processor.parameters, run_strings_collection)
                if not result:
                    logger.info(f"Job processor '{job_processor.code}' aborted")
                    return False
        return True


class OutputHandlerCollection(AbstractHandlerCollection):
    def output(self, job: Job, job_run_vars_collection: JobRunVarCollection):
        job_output: JobOutput
        for job_output in job.outputs:
            output_handler: AbstractHandler = self.get_by_code(job_output.code)
            if isinstance(output_handler, AbstractOutputHandler):
                output_handler.run(job_output.parameters, job_run_vars_collection)
