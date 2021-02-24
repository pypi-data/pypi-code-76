import pytest

from netcdf_scm.normalisation import NormaliserRunningMean, get_normaliser


@pytest.mark.parametrize(
    "key,expected_cls", (("21-yr-running-mean", NormaliserRunningMean),)
)
def test_get_normaliser(key, expected_cls):
    assert isinstance(get_normaliser(key), expected_cls)


def test_get_normaliser_error():
    error_msg = "Unrecognised key: 'junk'"
    with pytest.raises(ValueError, match=error_msg):
        get_normaliser("junk")
