import logging
from unittest.mock import MagicMock, Mock, call, patch

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.handlers.inputs.random_message_input import RandomMessageInput
from modular_message_bot.models.job_run import JobRunVar

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.handlers.inputs.random_message_input.logger")


def test_get_code():
    assert RandomMessageInput.get_code() == "random_message"


@patch("modular_message_bot.handlers.inputs.random_message_input.random_choice")
def test_run_input(mock_random_choice: MagicMock):
    # Given
    mock_random_choice.side_effect = ["Buongiorno!", "Adiós"]
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_vars_collection = Mock()
    vars_list = []
    vars_dict = {
        "greeting_en": "Good Morning!",
        "greeting_it": "Buongiorno!",
        "greeting_es": "Buenos días!",
        "morning_message": "Hi! {msg1}",
        "bye_en": "Bye",
        "bye_it": "Ciao",
        "bye_es": "Adiós",
        "afternoon_message": "Cya! {msg2}",
    }
    for key, value in vars_dict.items():
        vars_list.append(JobRunVar(code=key, value=value, interpolated_by_input_codes=[]))
    mock_job_run_vars_collection.get_all.return_value = vars_list
    parameters = {"match": {"msg1": "^greeting_", "msg2": "^bye_"}}

    # When
    module = RandomMessageInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    mock_job_run_vars_collection.interpolate.assert_has_calls(
        [call("msg1", "Buongiorno!", "random_message"), call("msg2", "Adiós", "random_message")]
    )


@patch("modular_message_bot.handlers.inputs.random_message_input.random_choice")
def test_run_input_no_match(mock_random_choice: MagicMock, mock_logger: MagicMock):
    # Given
    mock_random_choice.side_effect = ["Buongiorno!", "Adiós"]
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_vars_collection = Mock()
    vars_list = []
    vars_dict = {
        "greeting_en": "Good Morning!",
        "greeting_it": "Buongiorno!",
        "greeting_es": "Buenos días!",
        "morning_message": "Hi! {msg1}",
        "afternoon_message": "Cya! {msg2}",
    }
    for key, value in vars_dict.items():
        vars_list.append(JobRunVar(code=key, value=value, interpolated_by_input_codes=[]))
    mock_job_run_vars_collection.get_all.return_value = vars_list
    # fmt: off
    parameters = {
        "match": {
            "msg1": "^greeting_",
            "msg2": "^bye_"
        }
    }
    # fmt: on

    # When
    module = RandomMessageInput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_input(parameters, mock_job_run_vars_collection)

    # Then
    mock_job_run_vars_collection.interpolate.assert_called_once_with("msg1", "Buongiorno!", "random_message")
    mock_logger.warning.assert_called_once_with("random_message: No matching job strings")
