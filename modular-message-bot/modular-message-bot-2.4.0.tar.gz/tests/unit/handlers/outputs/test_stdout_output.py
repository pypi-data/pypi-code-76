from unittest.mock import MagicMock, Mock, patch

from modular_message_bot.handlers.outputs.stdout_output import StdoutOutput


def test_get_code():
    assert StdoutOutput.get_code() == "stdout"


def test_validate_job_config():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    mock_job_config.parameters = {"message": "http://www.google.com"}

    # When
    module = StdoutOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == ""


def test_validate_job_config_invalid_no_message():
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_config = Mock()
    mock_job_config.parameters = {}

    # When
    module = StdoutOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    result = module.validate_job_config(mock_job_config)

    # Then
    assert result == "'message' is required for 'stdout' output"


@patch("modular_message_bot.handlers.outputs.stdout_output.write_to_standard_out")
def test_run_output(write_to_standard_out_patch: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    parameters = {"message": "test of an example message here"}

    # When
    module = StdoutOutput(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    module.run_output(parameters)

    # Then
    write_to_standard_out_patch.assert_called_once_with("test of an example message here")
