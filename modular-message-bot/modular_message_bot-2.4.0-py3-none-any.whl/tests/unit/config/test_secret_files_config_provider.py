from unittest.mock import MagicMock, patch

import pytest

from modular_message_bot.config.config_collection import ConfigProviderKeyNotFoundException
from modular_message_bot.config.secret_files_config_provider import SecretFilesProvider


@patch("modular_message_bot.config.secret_files_config_provider.dir_files")
@patch("modular_message_bot.config.secret_files_config_provider.dir_exists")
def test_config_collection_get_keys(mock_dir_exists: MagicMock, mock_dir_files: MagicMock):
    # Given
    mock_dir_files.return_value = ["a", "b", "c"]
    mock_dir_exists.return_value = True
    config_provider = SecretFilesProvider(1000)

    # When
    keys = config_provider.get_keys()

    # Then
    assert keys == ["a", "b", "c"]
    mock_dir_exists.assert_called_with("/run/secrets")
    mock_dir_files.assert_called_with("/run/secrets")


@patch("modular_message_bot.config.secret_files_config_provider.dir_files")
@patch("modular_message_bot.config.secret_files_config_provider.dir_exists")
def test_config_collection_get_keys_no_dir(mock_dir_exists: MagicMock, mock_dir_files: MagicMock):
    # Given
    mock_dir_exists.return_value = False
    config_provider = SecretFilesProvider(1000)

    # When
    keys = config_provider.get_keys()

    # Then
    assert keys == []
    mock_dir_exists.assert_called_with("/run/secrets")
    mock_dir_files.assert_not_called()


@patch("modular_message_bot.config.secret_files_config_provider.dir_exists")
@patch("modular_message_bot.config.secret_files_config_provider.dir_files")
@patch("modular_message_bot.config.secret_files_config_provider.file_contents")
def test_dict_config_provider_get_value(
    mock_file_contents: MagicMock, mock_dir_files: MagicMock, mock_dir_exists: MagicMock
):
    # Given
    mock_dir_files.return_value = ["a", "b", "c"]
    mock_dir_exists.return_value = True
    mock_file_contents.return_value = "SecretConfigValueHere"
    config_provider = SecretFilesProvider(1000)

    # When
    result = config_provider.get_value("b")

    # Then
    assert result == "SecretConfigValueHere"
    mock_dir_exists.assert_called_with("/run/secrets")
    mock_dir_files.assert_called_with("/run/secrets")
    mock_file_contents.assert_called_with("/run/secrets/b")


@patch("modular_message_bot.config.secret_files_config_provider.dir_exists")
@patch("modular_message_bot.config.secret_files_config_provider.dir_files")
@patch("modular_message_bot.config.secret_files_config_provider.file_contents")
def test_dict_config_provider_get_value_missing(
    mock_file_contents: MagicMock, mock_dir_files: MagicMock, mock_dir_exists: MagicMock
):
    # Given
    mock_dir_files.return_value = ["a", "b", "c"]
    mock_dir_exists.return_value = True
    mock_file_contents.return_value = "SecretConfigValueHere"
    config_provider = SecretFilesProvider(1000)

    # When / Then
    with pytest.raises(
        ConfigProviderKeyNotFoundException,
        match="Config key 'I_DO_NOT_EXIST' not found in 'Secret Files Config Provider'",
    ):
        config_provider.get_value("I_DO_NOT_EXIST")

    # Then
    mock_dir_exists.assert_called_with("/run/secrets")
    mock_dir_files.assert_called_with("/run/secrets")
    mock_file_contents.assert_not_called()
