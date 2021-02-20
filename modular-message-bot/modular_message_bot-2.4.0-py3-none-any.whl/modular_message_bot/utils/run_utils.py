# This file contains a collection of helper functions that are not tested
import locale
import logging
import os
from typing import Tuple

from dotenv import load_dotenv

from modular_message_bot.config.config_collection import ConfigCollection
from modular_message_bot.factory import (
    build_boot_config_interpolator,
    build_dynamic_config_interpolator,
    build_init_config,
    build_input_handlers,
    build_job_string_interpolator,
    build_output_handlers,
    build_pre_handlers,
    build_processor_handlers,
)
from modular_message_bot.job_runner import JobRunner
from modular_message_bot.job_validator import JobValidator
from modular_message_bot.models.job import JobsCollection
from modular_message_bot.run_details_loader import get_jobs_collection, get_run_details, get_run_details_config_provider
from modular_message_bot.utils.common_utils import root_dir
from modular_message_bot.utils.module_util import get_extension


def run_init() -> ConfigCollection:
    """
    Initialisation code for all scripts
    :return: Config
    """
    extension = get_extension("run_init_extension")
    if extension:
        return extension()
    load_dotenv(dotenv_path=f"{root_dir()}/.env")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    config = build_init_config()
    return config


def set_locales(config: ConfigCollection):
    locale.setlocale(locale.LC_ALL, config.get("LOCALE_ALL"))


def bootstrap() -> Tuple[ConfigCollection, JobsCollection, JobRunner, JobValidator]:
    config = run_init()

    # Set locales
    set_locales(config)

    # String interpolators
    job_string_interpolator = build_job_string_interpolator()
    dynamic_config_interpolator = build_dynamic_config_interpolator(config)
    boot_config_interpolator = build_boot_config_interpolator(config)

    # Run Details (File, Folder, Dir etc)
    run_details = get_run_details(config)
    # Note: This means the run details config will only ever be able to be dynamically used (`$[`)
    run_details_interpolated = boot_config_interpolator.interpolate_dict(run_details)

    # Add Jobs config provider
    config.add_provider(get_run_details_config_provider(run_details_interpolated, 2000))

    # Jobs Collection
    jobs = get_jobs_collection(config, run_details_interpolated)

    # Handlers
    pre_handlers = build_pre_handlers(config, dynamic_config_interpolator, job_string_interpolator)
    input_handlers = build_input_handlers(config, dynamic_config_interpolator, job_string_interpolator)
    processor_handlers = build_processor_handlers(config, dynamic_config_interpolator, job_string_interpolator)
    output_handlers = build_output_handlers(config, dynamic_config_interpolator, job_string_interpolator)

    # Job Validator
    job_validator = JobValidator(pre_handlers, input_handlers, processor_handlers, output_handlers)

    # Job Handler
    job_runner = JobRunner(
        dynamic_config_interpolator=dynamic_config_interpolator,
        job_string_interpolator=job_string_interpolator,
        pre_handlers=pre_handlers,
        input_handlers=input_handlers,
        processor_handlers=processor_handlers,
        output_handlers=output_handlers,
    )

    return config, jobs, job_runner, job_validator
