import abc

import numpy as np
from numpy.core.numeric import asanyarray
from scipy.stats.distributions import (
    bernoulli,
    beta,
    binom,
    chi2,
    expon,
    f,
    gamma,
    geom,
    lognorm,
    norm,
    poisson,
    t,
)
from sklearn.neighbors import KernelDensity

from brad.exceptions import EmptyDataError

__all__ = ["NonParametricSampler", "ParametricSampler", "SmoothSampler"]

_DIST_LOOKUP = {
    d.name: d
    for d in [
        bernoulli,
        beta,
        binom,
        chi2,
        expon,
        f,
        gamma,
        geom,
        lognorm,
        norm,
        poisson,
        t,
    ]
}


class Sampler(abc.ABC):
    def __init__(self, data):
        self._data = asanyarray(data)

        if self._data.ndim == 0:
            raise ValueError("Parameter 'data' cannot be a scalar")
        elif self._data.size == 0:
            raise EmptyDataError("Supplied data is empty! Nothing to sample")

    @abc.abstractclassmethod
    def __iter__(self):
        """This method should yield samples from the sampler"""


class NonParametricSampler(Sampler):
    def __init__(self, data, *, max_buffer=1_000_000):
        super().__init__(data)
        self.sample_size = self._data.shape[0]
        self.max_buffer = max_buffer

    def __iter__(self):
        buffer_size = self.max_buffer - (self.max_buffer % self.sample_size)

        rng = np.random.default_rng()

        while True:
            buffer = rng.choice(self.sample_size, buffer_size)

            for batch in np.split(buffer, buffer_size // self.sample_size):
                yield self._data[batch]


class ParametricSampler(Sampler):
    def __init__(self, data, family: str):
        super().__init__(data)

        if self._data.ndim != 1:
            raise ValueError("Parametric samplers expect 1-d data.")

        if family in _DIST_LOOKUP:
            self.dist = _DIST_LOOKUP[family]
        else:
            raise ValueError(
                f"Invalid option '{family}' for parameter 'family'"
            )

        self.args = self.dist.fit(self._data)
        self.sample_size = self._data.shape[0]

    def __iter__(self):
        while True:
            yield self.dist.rvs(*self.args, size=self.sample_size)


class SmoothSampler(Sampler):
    def __init__(self, data, kernel: str = "gaussian", bandwidth: float = 0.2):
        if kernel not in {"gaussian", "tophat"}:
            raise ValueError(
                f"Invalid option '{kernel}' for parameter 'kernel'"
            )

        super().__init__(data)
        self.kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(
            self._data
        )
        self.sample_size = self._data.shape[0]

    def __iter__(self):
        while True:
            yield self.kde.sample(n_samples=self.sample_size)


class JackknifeSampler(Sampler):
    def __init__(self, data):
        super().__init__(data)
        self.sample_size = self._data.shape[0]

    def __iter__(self):
        for i in range(self.sample_size):
            yield np.delete(self._data, i, axis=0)


class BootknifeSampler(Sampler):
    def __init__(self, data, *, max_buffer=1_000_000):
        super().__init__(data)
        self.sample_size = self._data.shape[0]
        self.max_buffer = max_buffer

    def __iter__(self):
        buffer_size = self.max_buffer - (self.max_buffer % self.sample_size)

        rng = np.random.default_rng()

        # to ensure good stratification we randomise the order of the features
        # then delete them in order. stratification will be imperfect when done
        # in parallel by multiple workers, but it will be pretty good.
        order = rng.permutation(self.sample_size)
        idx = 0

        while True:
            buffer = rng.choice(self.sample_size - 1, buffer_size)

            for batch in np.split(buffer, buffer_size // self.sample_size):
                yield np.delete(self._data, order[idx], axis=0)[batch]
                idx = (idx + 1) % self.sample_size


class PermutationSampler(Sampler):
    def __iter__(self):
        rng = np.random.default_rng()
        shape = self._data.shape[0]

        while True:
            yield self._data[rng.permutation(shape)]
