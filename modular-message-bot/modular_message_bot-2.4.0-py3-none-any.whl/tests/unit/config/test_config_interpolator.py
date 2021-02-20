from modular_message_bot.config.config_collection import ConfigCollection, DictConfigProvider
from modular_message_bot.factory import build_dynamic_config_interpolator


def test_interpolate():
    # Given
    config = {"SOMETHING": "some thing", "ANOTHER": "another"}
    test_config = DictConfigProvider(config, "Unit Test Config", 1000)
    content = "I am a really long string with $[SOMETHING] here and $[ANOTHER] here"

    # When
    config = ConfigCollection()
    config.add_provider(test_config)
    interpolator = build_dynamic_config_interpolator(config)
    result = interpolator.interpolate(content)

    # Then
    assert result == "I am a really long string with some thing here and another here"


def test_interpolate_dict():
    # Given
    config = {"SOMETHING": "some thing", "ANOTHER": "another"}
    dictionary = {
        "level1": {"level2": "test1"},
        "level$[SOMETHING]here": "Value $[ANOTHER] here",
        "level $[SOMETHING]": {
            "level $[SOMETHING]": "$[ANOTHER]",
            "level$[SOMETHING]$[SOMETHING]$[SOMETHING]": {"$[SOMETHING]": "Hi $[ANOTHER]"},
        },
        "level $[ANOTHER] Number": 123,
        "level $[ANOTHER] here": ["I am $[ANOTHER]", "I $[SOMETHING] am", "I am something else"],
    }
    test_config = DictConfigProvider(config, "Unit Test Config", 1000)

    # When
    config = ConfigCollection()
    config.add_provider(test_config)
    interpolator = build_dynamic_config_interpolator(config)
    result = interpolator.interpolate_dict(dictionary)

    # Then
    assert result == {
        "level1": {"level2": "test1"},
        "levelsome thinghere": "Value another here",
        "level some thing": {
            "level some thing": "another",
            "levelsome thingsome thingsome thing": {"some thing": "Hi another"},
        },
        "level another Number": 123,
        "level another here": ["I am another", "I some thing am", "I am something else"],
    }
