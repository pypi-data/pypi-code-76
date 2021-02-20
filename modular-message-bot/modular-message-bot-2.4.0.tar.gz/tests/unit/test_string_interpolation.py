from modular_message_bot.string_interpolator import StringInterpolator


def test_interpolate():
    # Given
    message = "Hello {something} world {other}"
    replace_key = "something"
    replace_value = "I am something"
    string_interpolator = StringInterpolator("{", "}")

    # When
    result = string_interpolator.interpolate(message, replace_key, replace_value)

    # Then
    assert result == "Hello I am something world {other}"


def test_interpolate_unknown():
    # Given
    message = "Hello {something} world {other}"
    replace_key = "something_else"
    replace_value = "I should not be here"
    string_interpolator = StringInterpolator("{", "}")

    # When
    result = string_interpolator.interpolate(message, replace_key, replace_value)

    # Then
    assert result == "Hello {something} world {other}"


def test_is_interpolatable():
    # Given
    message = "Hello {something} world {other}"
    string_interpolator = StringInterpolator("{", "}")

    # When/Then
    assert string_interpolator.is_interpolatable(message, "something")
    assert string_interpolator.is_interpolatable(message, "other")
    assert not string_interpolator.is_interpolatable(message, "i_am_not_here")


def test_get_keys():
    # Given
    message = "Hello {something} world {other}"

    # When
    string_interpolator = StringInterpolator("{", "}")
    result = string_interpolator.get_keys(message)

    # When/Then
    assert result == ["something", "other"]


def test_interpolate_dict():
    # Given
    test_dict = {
        "level1": {"level2": "test1"},
        "level{A}here": "Value{A}here",
        "level{A}": {"level{A}{A}": "{A}", "level{A}{A}{A}": {"{A}": "Hi {A}"}},
        "level{A}Number": 123,
    }

    # When
    string_interpolator = StringInterpolator("{", "}")
    result_dict = string_interpolator.interpolate_dict(test_dict, "A", "B")

    # Then
    assert result_dict == {
        "level1": {"level2": "test1"},
        "levelBhere": "ValueBhere",
        "levelB": {"levelBB": "B", "levelBBB": {"B": "Hi B"}},
        "levelBNumber": 123,
    }
