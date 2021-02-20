"""Rounding Functions."""
import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies


class Floor(
    metaclass=_unaries.Unary,
    ipps_backend="Floor",
    numpy_backend=_numpy.floor,
    candidates=numpy_ipps.policies.no_complex_candidates,
    signed_len=True,
):
    """Floor Function."""

    pass


class Ceil(
    metaclass=_unaries.Unary,
    ipps_backend="Ceil",
    numpy_backend=_numpy.ceil,
    candidates=numpy_ipps.policies.no_complex_candidates,
    signed_len=True,
):
    """Floor Function."""

    pass


class Trunc(
    metaclass=_unaries.Unary,
    ipps_backend="Trunc",
    numpy_backend=_numpy.trunc,
    candidates=numpy_ipps.policies.no_complex_candidates,
    signed_len=True,
):
    """Trunc Function."""

    pass


class Frac(
    metaclass=_unaries.Unary,
    ipps_backend="Frac",
    candidates=numpy_ipps.policies.no_complex_candidates,
    signed_len=True,
):
    """Frac Function."""

    pass


class _RoundIPPSImpl:
    """Round Function -- Intel IPPS implementaion."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Round",
            (
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, src.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        _numpy.around(src.ndarray, out=dst.ndarray)


class _RoundNumpyImpl:
    """Round Function -- Numpy implementation."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Round",
            (
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        _numpy.around(src.ndarray, out=dst.ndarray)

    def _numpy_backend(self, src, dst):
        _numpy.around(src.ndarray, out=dst.ndarray)


class Round(
    metaclass=_selector.Selector,
    ipps_class=_RoundIPPSImpl,
    numpy_class=_RoundNumpyImpl,
    numpy_types_L2=(_numpy.float64,),
):
    """Round Function."""

    pass
