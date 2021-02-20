import re
from unittest.mock import Mock

import pytest

from modular_message_bot.utils.job_validation_utils import JobsInvalidException, run_validation


def test_run_validation():
    # Given
    mock_jobs = Mock()
    mock_job_validator = Mock()
    mock_job_validator.validate.return_value = ""

    # When
    run_validation(mock_job_validator, mock_jobs)

    # Then
    mock_job_validator.validate.assert_called_once_with(mock_jobs)


def test_run_validation_fails():
    # Given
    mock_jobs = Mock()
    mock_job_validator = Mock()
    mock_job_validator.validate.return_value = "You are missing 'xyz' parameter from 'abc'"

    # When / Then
    with pytest.raises(JobsInvalidException, match=re.escape("You are missing 'xyz' parameter from 'abc'")):
        run_validation(mock_job_validator, mock_jobs)

    # Then
    mock_job_validator.validate.assert_called_once_with(mock_jobs)
