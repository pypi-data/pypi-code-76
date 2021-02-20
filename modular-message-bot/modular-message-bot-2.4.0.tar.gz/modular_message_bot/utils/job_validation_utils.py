from modular_message_bot.job_validator import JobValidator
from modular_message_bot.models.job import JobsCollection


class JobsInvalidException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def run_validation(job_validator: JobValidator, jobs: JobsCollection):
    job_runner_validation = job_validator.validate(jobs)
    if job_runner_validation != "":
        raise JobsInvalidException(job_runner_validation)
