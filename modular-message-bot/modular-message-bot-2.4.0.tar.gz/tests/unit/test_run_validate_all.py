from unittest.mock import MagicMock, Mock, patch

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.run_validate_all import run


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.run_validate_all.logger")


@patch("modular_message_bot.run_validate_all.bootstrap")
def test_run_success(mock_bootstrap: MagicMock, mock_logger: MagicMock):
    # Given
    mock_config = Mock()
    mock_jobs = Mock()
    mock_job_runner = Mock()
    mock_job_validator = Mock()
    mock_bootstrap.return_value = (mock_config, mock_jobs, mock_job_runner, mock_job_validator)
    mock_job_validator.validate.return_value = ""

    # When
    run()

    # Then
    mock_job_validator.validate.assert_called_once_with(mock_jobs)
    mock_logger.info.assert_called_once_with("Jobs are valid!")


@patch("modular_message_bot.run_validate_all.exit")
@patch("modular_message_bot.run_validate_all.bootstrap")
def test_run_failure(mock_bootstrap: MagicMock, mock_exit: MagicMock, mock_logger: MagicMock):
    # Given
    mock_config = Mock()
    mock_jobs = Mock()
    mock_job_runner = Mock()
    mock_job_validator = Mock()
    mock_bootstrap.return_value = (mock_config, mock_jobs, mock_job_runner, mock_job_validator)
    mock_job_validator.validate.return_value = "'xyz' parameter is required for 'abc'"

    # When
    run()

    # Then
    mock_job_validator.validate.assert_called_once_with(mock_jobs)
    mock_logger.error.assert_called_once_with("'xyz' parameter is required for 'abc'")
    mock_exit.assert_called_once_with("Jobs are invalid")
    mock_logger.info.assert_not_called()
