import pytest

from foundation.error import BaseError


def test_can_raise_baseerror():
    with pytest.raises(BaseError):
        raise BaseError()
