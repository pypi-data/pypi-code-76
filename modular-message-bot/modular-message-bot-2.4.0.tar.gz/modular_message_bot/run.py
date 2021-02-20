"""
Script to run all jobs on a schedule using a blocking scheduler. This is the default run method (entrypoint) in the
Dockerfile.
Scheduling is done via a cron like syntax and is handled by [APScheduler](https://apscheduler.readthedocs.io/en/stable/)
Each job can have zero or more schedules.
Note: The day of the week is not the same as Linux, so it is recommended to instead use MON, FRI, MON-THR etc
"""
import io
import logging

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from modular_message_bot.config.constants import SCHEDULER_TIMEZONE_CFG_KEY
from modular_message_bot.job_runner import JobRunner
from modular_message_bot.models.job import Job
from modular_message_bot.utils.healthcheck_utils import healthcheck_liveness_file, healthcheck_readiness_file
from modular_message_bot.utils.job_validation_utils import run_validation
from modular_message_bot.utils.run_utils import bootstrap

logger = logging.getLogger(__name__)


def run():
    config, jobs, job_runner, job_validator = bootstrap()

    run_validation(job_validator, jobs)
    healthcheck_liveness_file(config)

    # Create and start the scheduler
    scheduler_timezone = config.get(SCHEDULER_TIMEZONE_CFG_KEY)
    logger.info(f"Scheduler timezone is '{scheduler_timezone}'")
    scheduler = BlockingScheduler(timezone=scheduler_timezone)

    # Add jobs
    job: Job
    for job in jobs.get_all():
        for schedule in job.schedules:
            trigger = CronTrigger.from_crontab(schedule, timezone=job.schedules_timezone)
            scheduler.add_job(run_job, trigger, args=[job_runner, job])

    # Run
    healthcheck_readiness_file(config)
    log_running_jobs(scheduler)
    scheduler.start()


def log_running_jobs(scheduler: BlockingScheduler):
    jobs_steam = io.StringIO("")
    scheduler.print_jobs(out=jobs_steam)
    logger.info(f"Jobs: {jobs_steam.getvalue()}")
    jobs_steam.close()


def run_job(job_runner: JobRunner, job: Job):
    job_runner.run_job(job)


if __name__ == "__main__":
    run()
