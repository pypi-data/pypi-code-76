from unittest.mock import MagicMock, Mock, patch

import pytest

from modular_message_bot.handlers.outputs.slack_output import SlackOutput


def test_get_code():
    assert SlackOutput.get_code() == "slack"


def test_validate_job_config():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    mock_job_config.parameters = {
        "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXX",
        "payload": {"text": "Hello World!"},
    }

    # When
    module = SlackOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == ""


def test_validate_job_config_invalid_no_payload():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    mock_job_config.parameters = {}

    # When
    module = SlackOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "'payload' is required for 'slack' output"


def test_validate_job_config_invalid_no_url():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    mock_job_config.parameters = {"payload": {}}

    # When
    module = SlackOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "'url' is required for 'slack' output"


def test_validate_job_config_invalid_no_payload_text():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    mock_job_config.parameters = {"url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXX", "payload": {}}

    # When
    module = SlackOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "payload.'text' is required for 'slack' output"


@patch("requests.post")
def test_output(mock_requests_post: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_request_response = Mock()
    mock_request_response.status_code = 200
    mock_requests_post.return_value = mock_request_response
    parameters = {
        "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXX",
        "payload": {"text": "Hello World!"},
    }

    # When
    module = SlackOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_output(parameters)

    # Then
    mock_requests_post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXXX", json={"text": "Hello World!"},
    )


@patch("requests.post")
def test_output_fails(mock_requests_post: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_request_response = Mock()
    mock_request_response.status_code = 500
    mock_request_response.content = "Something error here"
    mock_requests_post.return_value = mock_request_response
    parameters = {
        "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXX",
        "payload": {"text": "Hello World!"},
    }

    # When / Then
    module = SlackOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    with pytest.raises(Exception, match="ERROR: Response from request was 500\nSomething error here"):
        module.run_output(parameters)

    # Then
    mock_requests_post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXXX", json={"text": "Hello World!"},
    )
