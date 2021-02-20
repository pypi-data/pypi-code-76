"""Statistical Functions."""
import numpy as _numpy
import scipy.linalg as _linalg

import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies


class Max(
    metaclass=_unaries.Unary,
    ipps_backend="Max",
    numpy_backend=_numpy.max,
    candidates=(
        _numpy.int16,
        _numpy.int32,
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """Max Function.

    ``dst[0]  <-  Max( src )``
    """

    pass


class Min(
    metaclass=_unaries.Unary,
    ipps_backend="Min",
    numpy_backend=_numpy.min,
    candidates=(
        _numpy.int16,
        _numpy.int32,
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """Min Function.

    ``dst[0]  <-  Min( src )``
    """

    pass


def _norm_inf(a):
    return _linalg.norm(a, ord=_numpy.inf)


def _normDiff_inf(x1, x2):
    return _linalg.norm(x1 - x2, ord=_numpy.inf)


class Norm_Inf(
    metaclass=_unaries.Unary,
    ipps_backend="Norm-Inf",
    numpy_backend=_norm_inf,
    candidates=(
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """Norm Inf Function.

    ``dst[0]  <-  NormInf( src )``
    """

    pass


class NormDiff_Inf(
    metaclass=_binaries.Binary,
    ipps_backend="NormDiff-Inf",
    numpy_backend=_normDiff_inf,
    candidates=(
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """NormDiff Inf Function.

    ``dst[0]  <-  NormInf( src1 - src2 )``
    """

    pass


def _norm_l1(a):
    return _linalg.norm(a, ord=1)


def _normDiff_l1(x1, x2):
    return _linalg.norm(x1 - x2, ord=1)


class Norm_L1(
    metaclass=_unaries.Unary,
    ipps_backend="Norm-L1",
    numpy_backend=_norm_l1,
    candidates=(
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """Norm L1 Function.

    ``dst[0]  <-  NormL1( src )``
    """

    pass


class NormDiff_L1(
    metaclass=_binaries.Binary,
    ipps_backend="NormDiff-L1",
    numpy_backend=_normDiff_l1,
    candidates=(
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """NormDiff L1 Function.

    ``dst[0]  <-  NormL1( src1 - src2 )``
    """

    pass


def _norm_l2(a):
    return _linalg.norm(a, ord=2)


def _normDiff_l2(x1, x2):
    return _linalg.norm(x1 - x2, ord=2)


class Norm_L2(
    metaclass=_unaries.Unary,
    ipps_backend="Norm-L2",
    numpy_backend=_norm_l2,
    candidates=(
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """Norm L1 Function.

    ``dst[0]  <-  NormL2( src )``
    """

    pass


class NormDiff_L2(
    metaclass=_binaries.Binary,
    ipps_backend="NormDiff-L2",
    numpy_backend=_normDiff_l2,
    candidates=(
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """NormDiff L2 Function.

    ``dst[0]  <-  NormL2( src1 - src2 )``
    """

    pass


class Mean(
    metaclass=_unaries.Unary,
    ipps_backend="Mean",
    numpy_backend=_numpy.mean,
    policies=numpy_ipps.policies.Policies(
        bytes4=numpy_ipps.policies.TagPolicy.HINT_KEEP,
    ),
    candidates=(
        _numpy.float32,
        _numpy.float64,
        _numpy.complex64,
        _numpy.complex128,
    ),
    scalar=True,
):
    """Mean Function.

    ``dst[0]  <-  Sum( src ) / len( src )``
    """

    pass


def _std(a):
    return _numpy.std(a, ddof=1)


class StdDev(
    metaclass=_unaries.Unary,
    ipps_backend="StdDev",
    numpy_backend=_std,
    policies=numpy_ipps.policies.Policies(
        bytes4=numpy_ipps.policies.TagPolicy.HINT_KEEP,
    ),
    candidates=(
        _numpy.float32,
        _numpy.float64,
    ),
    scalar=True,
):
    """StdDev Function.

    ``dst[0]  <-  Sqrt( Sum( ( src - Mean( src ) )**2 / len( src ) ) )``
    """

    pass


class Sum(
    metaclass=_unaries.Unary,
    ipps_backend="Sum",
    numpy_backend=_numpy.sum,
    policies=numpy_ipps.policies.Policies(
        bytes2=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
        bytes4=numpy_ipps.policies.TagPolicy.HINT_SIGNED,
    ),
    candidates=(
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
        _numpy.float32,
        _numpy.float64,
        _numpy.complex64,
        _numpy.complex128,
    ),
    scalar=True,
):
    """Sum Function.

    ``dst[0]  <-  Sum( src )``
    """

    pass
