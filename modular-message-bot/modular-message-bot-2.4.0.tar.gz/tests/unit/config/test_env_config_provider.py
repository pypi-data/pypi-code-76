from unittest.mock import patch

import pytest

from modular_message_bot.config.config_collection import ConfigProviderKeyNotFoundException
from modular_message_bot.config.env_config_provider import build_env_config


@patch("modular_message_bot.config.env_config_provider.environ", {"a": "1", "b": "2", "c": "3"})
def test_config_collection_get_keys():
    # Given
    config_provider = build_env_config(1000)

    # When
    keys = config_provider.get_keys()

    # Then
    assert keys == ["a", "b", "c"]


@patch("modular_message_bot.config.env_config_provider.environ", {"a": "1", "b": "2", "c": "3"})
def test_dict_config_provider_get_value():
    # Given
    config_provider = build_env_config(1000)

    # When
    result = config_provider.get_value("b")

    # Then
    assert result == "2"


@patch("modular_message_bot.config.env_config_provider.environ", {"a": "1", "b": "2", "c": "3"})
def test_dict_config_provider_get_value_missing():
    # Given
    config_provider = build_env_config(1000)

    # When / Then
    with pytest.raises(
        ConfigProviderKeyNotFoundException, match="Config key 'I_DO_NOT_EXIST' not found in 'ENV config dict provider'",
    ):
        config_provider.get_value("I_DO_NOT_EXIST")
