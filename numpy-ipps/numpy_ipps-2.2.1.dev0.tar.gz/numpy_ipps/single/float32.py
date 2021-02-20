"""Functor on single element vectors for float32."""
import inspect
import sys

import numpy as _numpy

import numpy_ipps.exponential as _exponential
import numpy_ipps.floating as _floating
import numpy_ipps.policies
import numpy_ipps.special as _special
import numpy_ipps.trigonometric as _trigonometric
import numpy_ipps.utils


for module in [
    _exponential,
    _floating,
    _special,
    _trigonometric,
]:
    for name, cls in module.__dict__.items():
        if (
            not inspect.isclass(cls)
            or name.startswith("_")
            or _numpy.float32 not in cls.dtype_candidates
        ):
            continue

        setattr(
            sys.modules[__name__],
            name.lower(),
            cls(
                size=1,
                dtype=_numpy.float32,
                accuracy=numpy_ipps.policies.Accuracy.LEVEL_3
                if numpy_ipps.policies.Accuracy.LEVEL_3 in cls.ipps_accuracies
                else None,
            ),
        )


def new(value=_numpy.nan):
    """Create a new ndarray with a single element."""
    return numpy_ipps.utils.ndarray(
        _numpy.array([value], dtype=_numpy.float32)
    )
