from typing import Callable

import numpy as np
from numpy.core.numeric import asanyarray


def _map_statistic_onto_samples(
    sampler,
    statistic: Callable[[np.ndarray], np.ndarray],
    n_samples: int,
) -> np.ndarray:
    sampler = iter(sampler)
    sample = next(sampler)
    res = asanyarray(statistic(sample))
    buffer = np.zeros((n_samples,) + res.shape)
    buffer[0] = res

    for i, sample in enumerate(sampler, start=1):
        if i >= n_samples:
            break
        buffer[i] = asanyarray(statistic(sample))

    return buffer
