import pytest
import typing

from simio.utils import is_typing, cast_cap_words_to_lower


@pytest.mark.parametrize(
    "input_data, expected_result",
    (
        # fmt: off
        (
            int,
            False,
        ),
        (
            bool,
            False,
        ),
        (
            typing.Optional[int],
            True
        ),
        (
            typing.Dict[str, str],
            True
        ),
        # fmt: on
    ),
)
def test_is_typing(input_data, expected_result):
    result = is_typing(input_data)
    assert result == expected_result


@pytest.mark.parametrize(
    "input_data, expected_result",
    (
        # fmt: off
        (
            'SomeClassName',
            'some_class_name',
        ),
        (
            '',
            '',
        ),
        (
            'C',
            'c',
        ),
        (
            'AnotherClasS',
            'another_clas_s',
        )
        # fmt: on
    ),
)
def test_cast_cap_words_to_lower(input_data, expected_result):
    result = cast_cap_words_to_lower(input_data)
    assert result == expected_result
