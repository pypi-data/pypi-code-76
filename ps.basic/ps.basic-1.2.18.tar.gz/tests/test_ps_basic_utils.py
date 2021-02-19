"""Tests for the ps.basic.util Module."""
from ps.basic.utils import get_html_string, hms_string

import pytest


@pytest.mark.parametrize(
    "test_input1,expected1",
    [
        (
            {"A": "B"},
            "<table><tr><td>A</td><td>B</td></tr></table>",
        ),  # dictionary
        (
            {"A": {"B1": "B2"}},
            "<table><tr><td>A</td><td><table><tr><td>B1</td><td>B2</td></tr></table></td></tr></table>",  # noqa: E501
        ),
    ],
)
def test_html_string(test_input1, expected1):
    """[summary]

    :param test_input1: [description]
    :type test_input1: [type]
    :param expected1: [description]
    :type expected1: [type]
    """
    assert get_html_string(test_input1) == expected1


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (1, "00:00:01"),
        (61, "00:01:01"),
        (3661, "01:01:01"),
    ],
)
def test_hms_string(test_input, expected):
    """[summary]

    :param test_input: [description]
    :type test_input: [type]
    :param expected: [description]
    :type expected: [type]
    """
    assert hms_string(test_input) == expected
