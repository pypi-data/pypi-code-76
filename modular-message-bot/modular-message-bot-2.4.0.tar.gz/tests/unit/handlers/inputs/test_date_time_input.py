from datetime import datetime
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.handlers.inputs.date_time_input import DateTimeInput
from modular_message_bot.models.job_run import JobRunVar


@pytest.fixture(autouse=True)
def mock_date_time_input_datetime(mocker: MockerFixture):
    mock_dt = mocker.patch("modular_message_bot.handlers.inputs.date_time_input.datetime")
    mock_dt.utcnow.return_value = datetime(2020, 12, 29, 19, 51, 18, 342380)
    return mock_dt


def test_get_code():
    assert DateTimeInput.get_code() == "datetime"


def test_validate_job_config():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()

    # When
    module = DateTimeInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == ""


def test_validate_interpolated_message():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()

    # When
    module = DateTimeInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_run_var(JobRunVar(code="something", value="message", interpolated_by_input_codes=[]))

    # Then
    assert result == ""


def test_run_input():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_var_collection = Mock()
    # fmt: off
    parameters = {
        "var": "something",
        "timezone": "utc",
        "format": "%c"
    }
    # fmt: on

    # When
    module = DateTimeInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_var_collection)

    # Then
    mock_job_run_var_collection.interpolate.assert_called_once_with(
        "something", "Tue 29 Dec 2020 19:51:18 UTC", "datetime"
    )


def test_run_input_shifted():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_var_collection = Mock()
    # fmt: off
    parameters = {
        "var": "something",
        "timezone": "utc",
        "format": "%c",
        "add": {
            "days": 5,
            "minutes": 30
        },
        "sub": {
            "hours": 1,
            "seconds": 10
        }
    }
    # fmt: on

    # When
    module = DateTimeInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_var_collection)

    # Then
    mock_job_run_var_collection.interpolate.assert_called_once_with(
        "something", "Sun 03 Jan 2021 19:21:08 UTC", "datetime"
    )
