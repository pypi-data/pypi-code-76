import pytest

from stringliteral import StringLiteral


class AllowedVals(StringLiteral):
    LEFT = "left"
    RIGHT = "right"
    UP = "Up"


@pytest.mark.parametrize("value", ["left", "right"])
def test_contains(value):

    assert AllowedVals.contains(value)


def test_not_contains():
    """Containment check is case sensitive."""
    assert not AllowedVals.contains("up")


def test_value():
    assert AllowedVals.LEFT == "left"
