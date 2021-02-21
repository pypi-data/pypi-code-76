import functools
from typing import Callable, Optional

import numpy as np

from brad.core import _map_statistic_onto_samples
from brad.samplers import (
    BootknifeSampler,
    JackknifeSampler,
    NonParametricSampler,
    ParametricSampler,
    PermutationSampler,
    Sampler,
    SmoothSampler,
)

try:
    from importlib.metadata import (  # type: ignore
        PackageNotFoundError,
        version,
    )
except ModuleNotFoundError:
    # if using Python 3.7, import from the backport
    from importlib_metadata import (  # type: ignore
        PackageNotFoundError,
        version,
    )

try:
    __version__ = version("brad")
except PackageNotFoundError:
    # package is not installed
    pass


__all__ = [
    "bootknife",
    "bootstrap",
    "parametric_bootstrap",
    "permutation_test",
    "smooth_bootstrap",
]


def resample(
    sampler: Sampler,
    n_samples: int,
    *,
    statistic: Optional[Callable[[np.ndarray], np.ndarray]] = None,
):
    """
    Draw `n_samples` from `sampler` and optionally apply `statistic` to each
    sample. Used as a building block for all other resampling functions.

    Parameters
    ----------
    n_samples: int
        The number of samples to draw.
    sampler: Sampler
        A sampler from which samples will be drawn.
    statistic: callable, optional
        A statistic that can be applied to each sample. It not provided, then
        samples are returned untouched.
    """
    return _map_statistic_onto_samples(
        sampler, statistic or (lambda sample: sample), n_samples
    )


def bootstrap(
    data: np.ndarray,
    n_samples: int,
    *,
    statistic: Optional[Callable[[np.ndarray], np.ndarray]] = None,
) -> np.ndarray:
    """
    Generate bootstrap samples from data.

    Parameters
    ----------
    data: array_like
        Input data from which to draw bootstrap samples.
    n_samples: int
        The number of samples to draw.
    statistic: callable, optional.
        A function/statistic to apply to each bootstrap sample. If statistic is
        supplied then the returned array will have shape
        (n_samples, ) + f_return_shape.

    Returns
    -------
    numpy.ndarray
        An array of samples.
    """
    sampler = NonParametricSampler(data)
    return resample(sampler, n_samples, statistic=statistic)


def smooth_bootstrap(
    data,
    n_samples,
    *,
    kernel: str = "gaussian",
    bandwidth: float = 0.2,
    statistic=None,
):
    sampler = SmoothSampler(data, kernel=kernel, bandwidth=bandwidth)
    return resample(sampler, n_samples, statistic=statistic)


def parametric_bootstrap(data, n_samples, *, family: str, statistic=None):
    sampler = ParametricSampler(data, family=family)
    return resample(sampler, n_samples, statistic=statistic)


def permutation_test(
    data: np.ndarray, labels: np.ndarray, n_samples: int, *, statistic=None
) -> np.ndarray:
    """
    Randomly permute labels and apply statistic n_samples times.

    Parameters
    ----------
    data: array_like
        Input data with which to conduct permutation test.
    labels: array_like
        Labels must have x.shape[0] == labels.shape[0].
    n_samples: int
        The number of samples / permutations to draw.
    statistic: callable
        A function to apply to each bootstrap sample. The expected signature is
        (x, labels) -> stat.

    Returns
    -------
    numpy.ndarray
        An array of samples with shape (n_samples, ) + statistic_shape.
    """
    if data.shape[0] != labels.shape[0]:
        raise ValueError(
            "Shape mismatch: first dimension of data and labels should be the "
            "same size."
        )

    sampler = PermutationSampler(labels)

    statistic = functools.partial(
        statistic or (lambda data, labels: labels), data
    )
    return resample(sampler, n_samples, statistic=statistic)


def bootknife(
    data: np.ndarray,
    n_samples: int,
    *,
    statistic: Optional[Callable[[np.ndarray], np.ndarray]] = None,
) -> np.ndarray:
    """
    Generate bootknife samples from data.

    Parameters
    ----------
    data: array_like
        Input data from which to draw bootstrap samples.
    n_samples: int
        The number of samples to draw.
    statistic: callable, optional.
        A function/statistic to apply to each bootstrap sample. If statistic is
        supplied then the returned array will have shape
        (n_samples, ) + f_return_shape.

    Returns
    -------
    numpy.ndarray
        An array of samples.
    """
    sampler = BootknifeSampler(data)
    return resample(sampler, n_samples, statistic=statistic)


def jackknife(
    data: np.ndarray,
    *,
    statistic: Optional[Callable[[np.ndarray], np.ndarray]] = None,
) -> np.ndarray:
    """
    Generate jackknife samples from data.

    Parameters
    ----------

    - data: array_like.
        Input data from which to draw jackknife samples.
    - statistic: callable, optional.
        A function/statistic to apply to each sample. If statistic is supplied
        then the returned array will have shape (n_samples, ) + f_return_shape.

    Returns
    -------
    numpy.ndarray
        An array of samples.
    """
    sampler = JackknifeSampler(data)
    return resample(sampler, len(data), statistic=statistic)
