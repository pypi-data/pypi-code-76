import pytest

from modular_message_bot.config.config_collection import ConfigProviderKeyNotFoundException
from modular_message_bot.config.default_config_provider import build_default_config


def test_config_collection_get_keys():
    # Given
    config_provider = build_default_config(1000)

    # When
    keys = config_provider.get_keys()

    # Then
    assert keys == ["SCHEDULER_TIMEZONE", "LC_ALL"]


def test_dict_config_provider_get_value():
    # Given
    config_provider = build_default_config(1000)

    # When
    result_timezone = config_provider.get_value("SCHEDULER_TIMEZONE")
    result_lc_all = config_provider.get_value("LC_ALL")

    # Then
    assert result_timezone == "utc"
    assert result_lc_all == "en_US.utf8"


def test_dict_config_provider_get_value_missing():
    # Given
    config_provider = build_default_config(1000)

    # When / Then
    with pytest.raises(
        ConfigProviderKeyNotFoundException,
        match="Config key 'I_DO_NOT_EXIST' not found in 'Default config dict provider'",
    ):
        config_provider.get_value("I_DO_NOT_EXIST")
