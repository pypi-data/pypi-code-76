from modular_message_bot.utils.healthcheck_utils import healthcheck_liveness_file, healthcheck_readiness_file
from modular_message_bot.utils.job_validation_utils import run_validation
from modular_message_bot.utils.run_utils import bootstrap


def run():
    config, jobs, job_runner, job_validator = bootstrap()

    run_validation(job_validator, jobs)
    healthcheck_liveness_file(config)
    healthcheck_readiness_file(config)

    for job in jobs.get_all():
        job_runner.run_job(job)


if __name__ == "__main__":
    run()
