from unittest.mock import MagicMock, Mock, patch

from modular_message_bot.utils.healthcheck_utils import healthcheck_liveness_file, healthcheck_readiness_file


@patch("modular_message_bot.utils.healthcheck_utils.Path")
def test_healthcheck_liveness_file_on(mock_path: MagicMock):
    # Given
    mock_config = Mock()
    mock_config.get.return_value = "/tmp/liveness"

    # When
    healthcheck_liveness_file(mock_config)

    # Then
    mock_path.assert_called_once_with("/tmp/liveness")
    mock_path.return_value.touch.assert_called_once()


@patch("modular_message_bot.utils.healthcheck_utils.Path")
def test_healthcheck_liveness_file_off(mock_path: MagicMock):
    # Given
    mock_config = Mock()
    mock_config.get.return_value = ""

    # When
    healthcheck_liveness_file(mock_config)

    # Then
    mock_path.assert_not_called()


@patch("modular_message_bot.utils.healthcheck_utils.Path")
def test_healthcheck_readiness_file_file_on(mock_path: MagicMock):
    # Given
    mock_config = Mock()
    mock_config.get.return_value = "/tmp/readiness"

    # When
    healthcheck_readiness_file(mock_config)

    # Then
    mock_path.assert_called_once_with("/tmp/readiness")
    mock_path.return_value.touch.assert_called_once()


@patch("modular_message_bot.utils.healthcheck_utils.Path")
def test_healthcheck_readiness_file_off(mock_path: MagicMock):
    # Given
    mock_config = Mock()
    mock_config.get.return_value = ""

    # When
    healthcheck_readiness_file(mock_config)

    # Then
    mock_path.assert_not_called()
