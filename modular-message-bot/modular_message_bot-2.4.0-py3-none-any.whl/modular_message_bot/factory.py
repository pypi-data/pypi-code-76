from modular_message_bot.config.config_collection import ConfigCollection
from modular_message_bot.config.config_interpolator import ConfigInterpolator
from modular_message_bot.config.default_config_provider import build_default_config
from modular_message_bot.config.env_config_provider import build_env_config
from modular_message_bot.config.secret_files_config_provider import SecretFilesProvider
from modular_message_bot.handlers.handler_collections import (
    InputHandlerCollection,
    OutputHandlerCollection,
    PreHandlerCollection,
    ProcessorHandlerCollection,
)
from modular_message_bot.string_interpolator import StringInterpolator
from modular_message_bot.utils.module_util import get_handlers_module_definitions

# fmt: off


def build_pre_handlers(
        config: ConfigCollection,
        dynamic_config_interpolator: ConfigInterpolator,
        job_string_interpolator: StringInterpolator
) -> PreHandlerCollection:
    collection = PreHandlerCollection()
    for class_definition in get_handlers_module_definitions("pres"):
        collection.add_handler(class_definition(config, dynamic_config_interpolator, job_string_interpolator))
    return collection


def build_input_handlers(
        config: ConfigCollection,
        dynamic_config_interpolator: ConfigInterpolator,
        job_string_interpolator: StringInterpolator
) -> InputHandlerCollection:
    collection = InputHandlerCollection()
    for class_definition in get_handlers_module_definitions("inputs"):
        collection.add_handler(class_definition(config, dynamic_config_interpolator, job_string_interpolator))
    return collection


def build_processor_handlers(
        config: ConfigCollection,
        dynamic_config_interpolator: ConfigInterpolator,
        job_string_interpolator: StringInterpolator
) -> ProcessorHandlerCollection:
    collection = ProcessorHandlerCollection()
    for class_definition in get_handlers_module_definitions("processors"):
        collection.add_handler(class_definition(config, dynamic_config_interpolator, job_string_interpolator))
    return collection


def build_output_handlers(
        config: ConfigCollection,
        dynamic_config_interpolator: ConfigInterpolator,
        job_string_interpolator: StringInterpolator
) -> OutputHandlerCollection:
    collection = OutputHandlerCollection()
    for class_definition in get_handlers_module_definitions("outputs"):
        collection.add_handler(class_definition(config, dynamic_config_interpolator, job_string_interpolator))
    return collection


def build_init_config() -> ConfigCollection:
    config = ConfigCollection()
    config.add_provider(build_env_config(3000))
    config.add_provider(SecretFilesProvider(6000))
    config.add_provider(build_default_config(9000))
    return config


def build_job_string_interpolator():
    return StringInterpolator("{", "}")


def build_boot_config_interpolator(config: ConfigCollection) -> ConfigInterpolator:
    config_string_interpolator = StringInterpolator("${", "}")
    return ConfigInterpolator(
        config_string_interpolator,
        config
    )


def build_dynamic_config_interpolator(config: ConfigCollection) -> ConfigInterpolator:
    config_string_interpolator = StringInterpolator("$[", "]")
    return ConfigInterpolator(
        config_string_interpolator,
        config
    )

# fmt: on
