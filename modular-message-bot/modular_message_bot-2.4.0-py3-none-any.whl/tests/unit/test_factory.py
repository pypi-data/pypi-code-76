from unittest.mock import Mock, patch

from modular_message_bot.config.config_interpolator import ConfigInterpolator
from modular_message_bot.config.constants import LOCALE_ALL, SCHEDULER_TIMEZONE_CFG_KEY
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
from modular_message_bot.string_interpolator import StringInterpolator


def test_build_pre_handlers():
    # Given
    mock_config = Mock()
    dynamic_config_interpolator = Mock()
    job_string_interpolator = Mock()

    # When
    input_handlers_collection = build_pre_handlers(mock_config, dynamic_config_interpolator, job_string_interpolator)

    # Then
    assert len(input_handlers_collection.get_all()) >= 1


def test_build_input_handlers():
    # Given
    mock_config = Mock()
    dynamic_config_interpolator = Mock()
    job_string_interpolator = Mock()

    # When
    input_handlers_collection = build_input_handlers(mock_config, dynamic_config_interpolator, job_string_interpolator)

    # Then
    assert len(input_handlers_collection.get_all()) >= 2


def test_build_processor_handlers():
    # Given
    mock_config = Mock()
    dynamic_config_interpolator = Mock()
    job_str_interpolator = Mock()

    # When
    input_handlers_collection = build_processor_handlers(mock_config, dynamic_config_interpolator, job_str_interpolator)

    # Then
    assert len(input_handlers_collection.get_all()) >= 1


def test_build_output_handlers():
    # Given
    mock_config = Mock()
    dynamic_cfg_interpolator = Mock()
    job_string_interpolator = Mock()

    # When
    output_handlers_collection = build_output_handlers(mock_config, dynamic_cfg_interpolator, job_string_interpolator)

    # Then
    assert len(output_handlers_collection.get_all()) >= 3


@patch("modular_message_bot.config.env_config_provider.environ", {"a": "1", "b": "2", "c": "3"})
def test_build_init_config():
    # Given

    # When
    config = build_init_config()
    keys = config.get_keys()
    default_timezone = config.get(SCHEDULER_TIMEZONE_CFG_KEY)
    default_locale_all = config.get(LOCALE_ALL)
    a_value = config.get("a")
    b_value = config.get("b")
    c_value = config.get("c")

    # Then
    assert len(keys) == 5
    assert default_timezone == "utc"
    assert default_locale_all == "en_US.utf8"
    assert a_value == "1"
    assert b_value == "2"
    assert c_value == "3"


def test_build_boot_config_interpolator():
    # Given
    mock_config = Mock()

    # When
    result = build_boot_config_interpolator(mock_config)

    # Then
    assert isinstance(result, ConfigInterpolator)


def test_build_job_string_interpolator():
    # Given

    # When
    result = build_job_string_interpolator()

    # Then
    assert isinstance(result, StringInterpolator)


def test_build_dynamic_config_interpolator():
    # Given
    mock_config = Mock()

    # When
    result = build_dynamic_config_interpolator(mock_config)

    # Then
    assert isinstance(result, ConfigInterpolator)
