import base64
import logging
from os.path import splitext
from typing import Any, Dict

import yaml

from modular_message_bot.config.config_collection import AbstractConfigProvider, ConfigCollection, DictConfigProvider
from modular_message_bot.config.constants import SCHEDULER_TIMEZONE_CFG_KEY
from modular_message_bot.models.job import Job, JobInput, JobOutput, JobPre, JobProcessor, JobsCollection
from modular_message_bot.utils.common_utils import dir_files, file_contents, root_dir

logger = logging.getLogger(__name__)


def get_run_details(config: ConfigCollection) -> dict:
    run_details_list = get_run_details_list(config)
    return run_details_combine(run_details_list)


def get_run_details_list(config: ConfigCollection) -> list:
    run_details_list = []

    # Load config from env
    run_details = config.get("RUN_DETAILS_B64", "")
    if run_details != "":
        logger.info("Run Details: Loading from ENV")
        run_details_list.append(yaml.safe_load(base64.b64decode(run_details).decode("utf8")))

    # Load config from file
    run_details_file = config.get("RUN_DETAILS_FILE", "")
    if run_details_file != "":
        logger.info(f"Job Details: Loading from file {run_details_file}")
        run_details_list.append(yaml.safe_load(file_contents(run_details_file)))

    # Load config from dir
    run_details_dir = config.get("RUN_DETAILS_DIR", f"{root_dir()}/config")
    if run_details_dir != "":
        logger.info(f"Job Details: Loading from dir {run_details_dir}")
        run_details_list += get_run_details_from_dir(run_details_dir)

    # Done
    return run_details_list


def get_run_details_from_dir(job_config_dir: str) -> list:
    run_details_list = []
    for file in dir_files(job_config_dir):
        file_full = f"{job_config_dir}/{file}"
        _, file_extension = splitext(file_full)
        if file_extension in [".yaml", ".yml"]:
            run_details_list.append(yaml.safe_load(file_contents(file_full)))
    return run_details_list


def run_details_combine(run_details_list: list) -> dict:
    run_details: Dict[str, Any] = {"jobs": [], "config": {}}
    for run_detail_item in run_details_list:
        run_details["jobs"] += run_detail_item.get("jobs", [])
        run_details["config"] = {**run_details["config"], **run_detail_item.get("config", {})}
    return run_details


def get_run_details_config_provider(run_details: dict, priority: int) -> AbstractConfigProvider:
    return DictConfigProvider(run_details.get("config", {}), "Run Config Config Provider", priority)


def get_jobs_collection(config: ConfigCollection, run_details: dict) -> JobsCollection:
    jobs = JobsCollection()
    for job_config in run_details.get("jobs", []):
        jobs.add_job(map_job_config(job_config, config))
    return jobs


def map_job_config(job_config: dict, config: ConfigCollection) -> Job:
    if "schedule" not in job_config.keys():
        job_config["schedule"] = []

    schedule = job_config["schedule"]
    schedules = schedule if isinstance(schedule, list) else [schedule]
    pres = []
    for pre_raw in job_config.get("pres", []):
        pres.append(JobPre(pre_raw.get("code"), pre_raw.get("parameters", {})))
    inputs = []
    for inputs_raw in job_config.get("inputs", []):
        inputs.append(JobInput(inputs_raw.get("code"), inputs_raw.get("parameters", {})))
    processors = []
    for processor_raw in job_config.get("processors", []):
        processors.append(JobProcessor(processor_raw.get("code"), processor_raw.get("parameters", {})))
    outputs = []
    for outputs_raw in job_config.get("outputs", []):
        outputs.append(JobOutput(outputs_raw.get("code"), outputs_raw.get("parameters", {})))
    return Job(
        config=config,
        id=job_config.get("id", ""),
        schedules=schedules,
        schedules_timezone=job_config.get("schedule-timezone", config.get(SCHEDULER_TIMEZONE_CFG_KEY)),
        pres=pres,
        vars=job_config.get("vars", {}),
        inputs=inputs,
        processors=processors,
        outputs=outputs,
    )
