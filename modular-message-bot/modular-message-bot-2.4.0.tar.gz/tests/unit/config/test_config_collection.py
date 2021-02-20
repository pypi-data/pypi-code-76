from unittest.mock import Mock

import pytest

from modular_message_bot.config.config_collection import (
    ConfigCollection,
    ConfigKeyNoProviderException,
    ConfigProviderKeyNotFoundException,
    DictConfigProvider,
)


def test_config_collection_get_or_fail():
    # Given
    config = ConfigCollection()

    provider1 = Mock()
    provider1.get_priority.return_value = 1
    provider1.get_keys.return_value = ["a1", "b1", "c1"]
    config.add_provider(provider1)

    provider2 = Mock()
    provider2.get_priority.return_value = 2
    provider2.get_keys.return_value = ["a2", "b2", "c2"]
    provider2.get_value.return_value = "The result"
    config.add_provider(provider2)

    # When
    result = config.get_or_fail("b2")

    # Then
    assert result == "The result"
    provider1.get_keys.assert_called_once()
    provider1.get_value.assert_not_called()
    provider2.get_keys.assert_called_once()
    provider2.get_value.assert_called_once_with("b2")


def test_config_collection_get_or_fail_failure():
    # Given
    config = ConfigCollection()

    provider1 = Mock()
    provider1.get_priority.return_value = 1
    provider1.get_keys.return_value = ["a1", "b1", "c1"]
    config.add_provider(provider1)

    provider2 = Mock()
    provider2.get_priority.return_value = 2
    provider2.get_keys.return_value = ["a2", "b2", "c2"]
    provider2.get_value.return_value = "The result"

    config.add_provider(provider2)

    # When / Then
    with pytest.raises(
        ConfigKeyNoProviderException, match="Config key 'a3' not found in any config providers",
    ):
        config.get_or_fail("a3")

    # Then
    provider1.get_keys.assert_called_once()
    provider1.get_value.assert_not_called()
    provider2.get_keys.assert_called_once()
    provider2.get_value.assert_not_called()


def test_config_collection_get():
    # Given
    config = ConfigCollection()

    provider1 = Mock()
    provider1.get_priority.return_value = 1
    provider1.get_keys.return_value = ["a1", "b1", "c1"]
    config.add_provider(provider1)

    provider2 = Mock()
    provider2.get_priority.return_value = 2
    provider2.get_keys.return_value = ["a2", "b2", "c2"]
    provider2.get_value.return_value = "The result"
    config.add_provider(provider2)

    # When
    result = config.get("b2", "default value")

    # Then
    assert result == "The result"
    provider1.get_keys.assert_called_once()
    provider1.get_value.assert_not_called()
    provider2.get_keys.assert_called_once()
    provider2.get_value.assert_called_once_with("b2")


def test_config_collection_get_default():
    # Given
    config = ConfigCollection()

    provider1 = Mock()
    provider1.get_priority.return_value = 1
    provider1.get_keys.return_value = ["a1", "b1", "c1"]
    config.add_provider(provider1)

    provider2 = Mock()
    provider2.get_priority.return_value = 2
    provider2.get_keys.return_value = ["a2", "b2", "c2"]
    provider2.get_value.return_value = "The result"
    config.add_provider(provider2)

    # When
    result = config.get("a3", "default value")

    # Then
    assert result == "default value"
    provider1.get_keys.assert_called_once()
    provider1.get_value.assert_not_called()
    provider2.get_keys.assert_called_once()
    provider2.get_value.assert_not_called()


def test_config_collection_get_keys():
    # Given
    config = {"a": "1", "b": "2", "c": "3"}
    dict_config = DictConfigProvider(config, "test dict provider", 1000)

    # When
    keys = dict_config.get_keys()

    # Then
    assert keys == ["a", "b", "c"]


def test_dict_config_provider_get_value():
    # Given
    config = {"a": "1", "b": "2", "c": "3"}
    dict_config = DictConfigProvider(config, "test dict provider", 1000)

    # When
    result = dict_config.get_value("a")

    # Then
    assert result == "1"


def test_dict_config_provider_get_value_missing():
    # Given
    config = {"a": "1", "b": "2", "c": "3"}
    dict_config = DictConfigProvider(config, "test dict provider", 1000)

    # When / Then
    with pytest.raises(
        ConfigProviderKeyNotFoundException, match="Config key 'd' not found in 'test dict provider'",
    ):
        dict_config.get_value("d")
