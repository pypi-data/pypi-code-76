from unittest.mock import MagicMock, Mock, patch

from modular_message_bot.handlers.pres.chance_pre import ChancePre


def test_get_code():
    assert ChancePre.get_code() == "chance"


@patch("modular_message_bot.handlers.pres.chance_pre.randint")
def test_run_success(mock_randint: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_vars_collection = Mock()
    mock_randint.return_value = 40
    parameters = {"percentage": 50}

    # When
    pre = ChancePre(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    continue_result = pre.run(parameters, mock_job_run_vars_collection)

    # Then
    assert continue_result
    mock_randint.assert_called_once_with(0, 100)


@patch("modular_message_bot.handlers.pres.chance_pre.randint")
def test_run_failure(mock_randint: MagicMock):
    # Given
    mock_config = Mock()
    mock_dynamic_config_interpolator = Mock()
    mock_job_string_interpolator = Mock()
    mock_job_run_vars_collection = Mock()
    mock_randint.return_value = 70
    parameters = {"percentage": 50}

    # When
    pre = ChancePre(mock_config, mock_dynamic_config_interpolator, mock_job_string_interpolator)
    is_continue = pre.run(parameters, mock_job_run_vars_collection)

    # Then
    assert not is_continue
    mock_randint.assert_called_once_with(0, 100)
