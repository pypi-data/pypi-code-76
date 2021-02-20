import re
from unittest.mock import MagicMock, Mock

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.handlers.outputs.pushover_output import PushoverOutput


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.outputs.pushover_output.logger")


@pytest.fixture(autouse=True)
def mock_request_post(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.outputs.pushover_output.request_post")


def test_get_code():
    assert PushoverOutput.get_code() == "pushover"


def test_validate_job_config():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "token": "azGDORePK8gMaC0QOYAMyEEuzJnyUi",
        "user": "uQiRzpo4DXghDmr9QzzfQu27cmVRsG",
        "message": "Hello World!!!",
    }
    # fmt: on

    # When
    module = PushoverOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == ""


def test_validate_job_config_no_token():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "user": "uQiRzpo4DXghDmr9QzzfQu27cmVRsG",
        "message": "Hello World!!!",
    }
    # fmt: on

    # When
    module = PushoverOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "'token' is required for 'pushover' output. Please see https://pushover.net/api"


def test_validate_job_config_no_user():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "token": "azGDORePK8gMaC0QOYAMyEEuzJnyUi",
        "message": "Hello World!!!",
    }
    # fmt: on

    # When
    module = PushoverOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "'user' is required for 'pushover' output. Please see https://pushover.net/api"


def test_validate_job_config_no_message():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    # fmt: off
    mock_job_config.parameters = {
        "token": "azGDORePK8gMaC0QOYAMyEEuzJnyUi",
        "user": "uQiRzpo4DXghDmr9QzzfQu27cmVRsG",
    }
    # fmt: on

    # When
    module = PushoverOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "'message' is required for 'pushover' output. Please see https://pushover.net/api"


def test_run_output(mock_request_post: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    parameters = {
        "token": "azGDORePK8gMaC0QOYAMyEEuzJnyUi",
        "user": "uQiRzpo4DXghDmr9QzzfQu27cmVRsG",
        "message": "Hello World!!!",
    }
    mock_request_post.return_value.status_code = 200

    # When
    module = PushoverOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_output(parameters)

    # Then
    mock_request_post.assert_called_once_with(
        "https://api.pushover.net/1/messages.json", headers={"Content-Type": "application/json"}, json=parameters
    )


def test_run_output_full(mock_request_post: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    parameters = {
        "token": "azGDORePK8gMaC0QOYAMyEEuzJnyUi",
        "user": "uQiRzpo4DXghDmr9QzzfQu27cmVRsG",
        "message": "Hello World!!!",
        "device": "droid2",
        "title": "Direct message from @someuser",
        "url": "twitter://direct_message?screen_name=someuser",
        "url_title": "Reply to @someuser",
        "priority": "1",
        "sound": "incoming",
        "timestamp": "1331249662",
    }
    mock_request_post.return_value.status_code = 200

    # When
    module = PushoverOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_output(parameters)

    # Then
    mock_request_post.assert_called_once_with(
        "https://api.pushover.net/1/messages.json", headers={"Content-Type": "application/json"}, json=parameters
    )


def test_run_output_errors(mock_request_post: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    parameters = {
        "token": "azGDORePK8gMaC0QOYAMyEEuzJnyUi",
        "user": "uQiRzpo4DXghDmr9QzzfQu27cmVRsG",
        "message": "Hello World!!!",
    }
    api_response = (
        "{"
        '"user":"invalid",'
        '"errors":["user identifier is invalid"],'
        '"status":0,"request":"5042853c-402d-4a18-abcb-168734a801de"'
        "}"
    )
    mock_request_post.return_value.status_code = 421
    mock_request_post.return_value.content = api_response

    # When
    module = PushoverOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)

    # When/Then
    with pytest.raises(Exception, match=re.escape(f"ERROR: Response failure 421\n{api_response}")):
        module.run_output(parameters)

    # Then
    mock_request_post.assert_called_once_with(
        "https://api.pushover.net/1/messages.json",
        headers={"Content-Type": "application/json"},
        json={
            "token": "azGDORePK8gMaC0QOYAMyEEuzJnyUi",
            "user": "uQiRzpo4DXghDmr9QzzfQu27cmVRsG",
            "message": "Hello World!!!",
        },
    )
