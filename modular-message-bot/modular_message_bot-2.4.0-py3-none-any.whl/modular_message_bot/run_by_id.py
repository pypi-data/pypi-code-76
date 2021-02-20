"""
Runs a specific job by id
i.e. `python3 -m modular_message_bot.run_by_id --id=$1`
"""
import argparse

from modular_message_bot.utils.healthcheck_utils import healthcheck_liveness_file, healthcheck_readiness_file
from modular_message_bot.utils.job_validation_utils import run_validation
from modular_message_bot.utils.run_utils import bootstrap


def run(job_id: str):
    config, jobs, job_runner, job_validator = bootstrap()

    run_validation(job_validator, jobs)
    healthcheck_liveness_file(config)

    job = jobs.get_by_id(job_id)
    healthcheck_readiness_file(config)

    job_runner.run_job(job)


def get_args() -> dict:
    """
    Gets the input args
    :return: dict
    """
    parser = argparse.ArgumentParser()  # NOSONAR - This is user data
    parser.add_argument(
        "--id", required=True, default="", help="The job id to run.",
    )
    args_dict = parser.parse_args().__dict__
    return {"job_id": str(args_dict["id"])}


if __name__ == "__main__":
    args = get_args()
    run(**args)
