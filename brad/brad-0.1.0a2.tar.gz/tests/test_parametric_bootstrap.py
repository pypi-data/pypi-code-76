import numpy as np
import pytest
from scipy.stats.distributions import lognorm, norm

from brad import parametric_bootstrap
from brad.exceptions import EmptyDataError

from .helpers import RANDOM_10x1, RANDOM_10x5, safe_mean

dist_names = [d.name for d in [lognorm, norm]]


@pytest.mark.parametrize("n_samples", [2, 7, 102])
@pytest.mark.parametrize("family", dist_names)
def test_shape_parametric_bootstrap(n_samples, family):
    data = RANDOM_10x1
    shape = data.shape

    assert parametric_bootstrap(data, n_samples, family=family).shape == (
        n_samples,
        shape[0],
    )
    assert parametric_bootstrap(
        data, n_samples, family=family, statistic=safe_mean
    ).shape == (n_samples,)


def test_empty_dataset():
    empty_dataset = np.arange(0)

    with pytest.raises(
        EmptyDataError, match="Supplied data is empty! Nothing to sample"
    ):
        parametric_bootstrap(empty_dataset, 1, family="norm")


def test_scalar_dataset():
    scalar_dataset = np.array(0)

    with pytest.raises(
        ValueError, match="Parameter 'data' cannot be a scalar"
    ):
        parametric_bootstrap(scalar_dataset, 1, family="norm")


def test_1d_data():
    with pytest.raises(
        ValueError, match="Parametric samplers expect 1-d data."
    ):
        parametric_bootstrap(RANDOM_10x5, 1, family="norm")


def test_invalid_family():
    with pytest.raises(ValueError):
        parametric_bootstrap(RANDOM_10x1, 1, family="invalid-family")
