from unittest.mock import MagicMock, Mock, patch

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.handlers.outputs.easy_http_output import EasyHttpOutput


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.outputs.easy_http_output.logger")


def test_get_code():
    assert EasyHttpOutput.get_code() == "easy_http"


def test_validate_job_config():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    mock_job_config.parameters = {"url": "http://www.example.com"}

    # When
    module = EasyHttpOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == ""


def test_validate_job_config_invalid_no_url():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    mock_job_config.parameters = {}

    # When
    module = EasyHttpOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "'url' is required for 'easy_http' output"


@patch("modular_message_bot.handlers.outputs.easy_http_output.requests.request")
def test_run_output(mock_requests: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_requests_response = Mock()
    mock_requests_response.status_code = 200
    mock_requests.return_value = mock_requests_response
    parameters = {
        "url": "http://127.0.0.1:12345/display",
        "method": "get",
        "ignore-failure": False,
        "args": {"headers": {"Auth-Token": "abc123"}, "data": {"message": "Hello World!!!", "duration": "10000"}},
    }

    # When
    module = EasyHttpOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_output(parameters)

    # Then
    mock_requests.assert_called_once_with(
        "get",
        "http://127.0.0.1:12345/display",
        headers={"Auth-Token": "abc123"},
        data={"message": "Hello World!!!", "duration": "10000"},
    )


@patch("modular_message_bot.handlers.outputs.easy_http_output.requests.request")
def test_run_failure(mock_requests: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_requests_response = Mock()
    mock_requests_response.status_code = 500
    mock_requests_response.content = "Something something error"
    mock_requests.return_value = mock_requests_response
    parameters = {
        "url": "http://127.0.0.1:12345/display",
        "method": "get",
        "ignore-failure": False,
        "args": {"json": {"message": "Hello"}},
    }

    # When / Then
    module = EasyHttpOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    with pytest.raises(Exception, match="ERROR: Response failure 500\nSomething something error"):
        module.run_output(parameters)

    # Then
    mock_requests.assert_called_once_with(
        "get", "http://127.0.0.1:12345/display", json={"message": "Hello"},
    )


@patch("modular_message_bot.handlers.outputs.easy_http_output.requests.request")
def test_run_failure_ignored(mock_requests: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_requests_response = Mock()
    mock_requests_response.status_code = 500
    mock_requests_response.content = "Something something error"
    mock_requests.return_value = mock_requests_response
    parameters = {
        "url": "http://127.0.0.1:12345/display",
        "method": "get",
        "ignore-failure": True,
        "args": {"json": {"message": "Hello"}},
    }

    # When
    module = EasyHttpOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_output(parameters)

    # Then
    mock_requests.assert_called_once_with(
        "get", "http://127.0.0.1:12345/display", json={"message": "Hello"},
    )
