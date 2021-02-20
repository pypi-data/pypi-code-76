import logging
from sys import exit

from modular_message_bot.utils.run_utils import bootstrap

logger = logging.getLogger(__name__)


def run():
    config, jobs, job_runner, job_validator = bootstrap()
    validation_result = job_validator.validate(jobs)
    if validation_result != "":
        logger.error(validation_result)
        exit("Jobs are invalid")
    else:
        logger.info("Jobs are valid!")


if __name__ == "__main__":
    run()
