from unittest.mock import Mock

from modular_message_bot.handlers.processors.regex_match_one_abort_processor import RegexMatchOneAbortProcessor
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection


def test_get_code():
    # Given

    # When
    result = RegexMatchOneAbortProcessor.get_code()

    # Then
    assert result == "regex_match_one_abort"


def test_process_match_all():
    # Given
    # fmt: off
    vars_dict = {
        "weather_edi": "The weather in Edinburgh is rain",
        "weather_gla": "The weather in Glasgow is rain",
    }
    parameters = {
        "match": {
            "weather_edi": "rain",
            "weather_gla": "rain",
        }
    }
    expected_is_continue = False
    # fmt: on

    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_str_interpolator = Mock()
    job_run_vars_collection = JobRunVarCollection(job_var_interpolator=Mock())
    for key, value in vars_dict.items():
        job_run_vars_collection.add_job_run_var(JobRunVar(code=key, value=value, interpolated_by_input_codes=[]))

    # When
    processor = RegexMatchOneAbortProcessor(mock_config, mock_dynamic_config_interpolator, mock_job_str_interpolator)
    is_continue = processor.process(parameters, job_run_vars_collection)

    # Then
    assert is_continue == expected_is_continue


def test_process_match_first():
    # Given
    # fmt: off
    vars_dict = {
        "weather_edi": "The weather in Edinburgh is rain",
        "weather_gla": "The weather in Glasgow is sun",
    }
    parameters = {
        "match": {
            "weather_edi": "rain",
            "weather_gla": "rain",
        }
    }
    expected_is_continue = False
    # fmt: on

    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    job_run_vars_collection = JobRunVarCollection(job_var_interpolator=Mock())
    for key, value in vars_dict.items():
        job_run_vars_collection.add_job_run_var(JobRunVar(code=key, value=value, interpolated_by_input_codes=[]))

    # When
    processor = RegexMatchOneAbortProcessor(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    is_continue = processor.process(parameters, job_run_vars_collection)

    # Then
    assert is_continue == expected_is_continue


def test_process_match_second():
    # Given
    # fmt: off
    vars_dict = {
        "weather_edi": "The weather in Edinburgh is sun",
        "weather_gla": "The weather in Glasgow is rain",
    }
    parameters = {
        "match": {
            "weather_edi": "rain",
            "weather_gla": "rain",
        }
    }
    expected_is_continue = False
    # fmt: on

    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    job_run_vars_collection = JobRunVarCollection(job_var_interpolator=Mock())
    for key, value in vars_dict.items():
        job_run_vars_collection.add_job_run_var(JobRunVar(code=key, value=value, interpolated_by_input_codes=[]))

    # When
    processor = RegexMatchOneAbortProcessor(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    is_continue = processor.process(parameters, job_run_vars_collection)

    # Then
    assert is_continue == expected_is_continue


def test_process_match_none():
    # Given
    # fmt: off
    vars_dict = {
        "weather_edi": "The weather in Edinburgh is sun",
        "weather_gla": "The weather in Glasgow is sun",
    }
    parameters = {
        "match": {
            "weather_edi": "rain",
            "weather_gla": "rain",
        }
    }
    expected_is_continue = True
    # fmt: on

    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    job_run_vars_collection = JobRunVarCollection(job_var_interpolator=Mock())
    for key, value in vars_dict.items():
        job_run_vars_collection.add_job_run_var(JobRunVar(code=key, value=value, interpolated_by_input_codes=[]))

    # When
    processor = RegexMatchOneAbortProcessor(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    is_continue = processor.process(parameters, job_run_vars_collection)

    # Then
    assert is_continue == expected_is_continue
