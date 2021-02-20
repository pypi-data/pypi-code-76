from unittest.mock import Mock

from modular_message_bot.handlers.processors.regex_match_all_continue_processor import RegexMatchAllContinueProcessor
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection


def test_get_code():
    # Given

    # When
    result = RegexMatchAllContinueProcessor.get_code()

    # Then
    assert result == "regex_match_all_continue"


def test_process_match_all():
    # Given
    # fmt: off
    vars_dict = {
        "weather_edi": "The weather in Edinburgh is clouds",
        "weather_gla": "The weather in Glasgow is clouds",
    }
    parameters = {
        "match": {
            "weather_edi": "clouds",
            "weather_gla": "clouds",
        }
    }
    expected_is_continue = True
    # fmt: on

    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_str_interpolator = Mock()
    job_run_vars_collection = JobRunVarCollection(job_var_interpolator=Mock())
    for key, value in vars_dict.items():
        job_run_vars_collection.add_job_run_var(JobRunVar(code=key, value=value, interpolated_by_input_codes=[]))

    # When
    processor = RegexMatchAllContinueProcessor(mock_config, mock_dynamic_config_interpolator, mock_job_str_interpolator)
    is_continue = processor.process(parameters, job_run_vars_collection)

    # Then
    assert is_continue == expected_is_continue


def test_process_match_first():
    # Given
    # fmt: off
    vars_dict = {
        "weather_edi": "The weather in Edinburgh is clouds",
        "weather_gla": "The weather in Glasgow is sun",
    }
    parameters = {
        "match": {
            "weather_edi": "clouds",
            "weather_gla": "clouds",
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
    processor = RegexMatchAllContinueProcessor(mock_config, mock_dynamic_config_interpolator, mock_job_str_interpolator)
    is_continue = processor.process(parameters, job_run_vars_collection)

    # Then
    assert is_continue == expected_is_continue


def test_process_match_second():
    # Given
    # fmt: off
    vars_dict = {
        "weather_edi": "The weather in Edinburgh is sun",
        "weather_gla": "The weather in Glasgow is clouds",
    }
    parameters = {
        "match": {
            "weather_edi": "clouds",
            "weather_gla": "clouds",
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
    processor = RegexMatchAllContinueProcessor(mock_config, mock_dynamic_config_interpolator, mock_job_str_interpolator)
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
            "weather_edi": "clouds",
            "weather_gla": "clouds",
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
    processor = RegexMatchAllContinueProcessor(mock_config, mock_dynamic_config_interpolator, mock_job_str_interpolator)
    is_continue = processor.process(parameters, job_run_vars_collection)

    # Then
    assert is_continue == expected_is_continue
