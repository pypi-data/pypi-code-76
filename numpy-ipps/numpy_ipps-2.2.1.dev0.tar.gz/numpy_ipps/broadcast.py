"""Arithmetic  Functions."""
import enum as _enum

import numpy as _numpy

import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


_binaryInt_candidates = (
    _numpy.uint8,
    _numpy.int16,
    _numpy.uint16,
    _numpy.int32,
    _numpy.float32,
    _numpy.float64,
    _numpy.complex64,
)
_Add_candidates = (
    _numpy.int8,
    _numpy.uint8,
    _numpy.int16,
    _numpy.uint16,
    _numpy.int32,
    _numpy.uint32,
    _numpy.float32,
    _numpy.float64,
    _numpy.complex64,
)


class Polarity(_enum.Enum):
    """Polarity enumeration."""

    NORMAL = 1
    REVERSE = 2


class _AddCIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="AddC",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
        bytes4=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
        bytes8=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
    ),
    candidates=_Add_candidates,
):
    """AddC Function -- Intel IPPS implementation."""

    pass


class _AddCNumpyImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="AddC",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
        bytes4=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
        bytes8=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
    ),
    candidates=_Add_candidates,
    force_numpy=True,
):
    """AddC Function -- Numpy implementation."""

    pass


class AddC(
    metaclass=_selector.Selector,
    ipps_class=_AddCIPPSImpl,
    numpy_class=_AddCNumpyImpl,
    numpy_types_L2=(
        _numpy.int32,
        _numpy.uint32,
    ),
    numpy_types_L1=(_numpy.int8,),
):
    """AddC Function.

    ``dst[n]  <-  src[n] + value``
    """

    pass


class AddC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="AddC_I",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
        bytes4=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
    ),
    candidates=_Add_candidates,
):
    """AddC_I Function.

    ``src_dst[n]  <-  src_dst[n] + value``
    """

    pass


class _MulCIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="MulC",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """MulC Function -- Intel IPPS implementation."""

    pass


class _MulCNumpyImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="MulC",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """MulC Function -- Numpy implementation."""

    pass


class MulC(
    metaclass=_selector.Selector,
    ipps_class=_MulCIPPSImpl,
    numpy_class=_MulCNumpyImpl,
    numpy_types_L1=(
        _numpy.uint8,
        _numpy.complex64,
    ),
):
    """MulC Function.

    ``dst[n]  <-  src[n] * value``
    """

    pass


class MulC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="MulC_I",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=(
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.float32,
        _numpy.float64,
    ),
):
    """MulC_I Function.

    ``src_dst[n]  <-  src_dst[n] * value``
    """

    pass


class _SubCIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="SubC",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """SubC Function -- Intel IPPS implementation."""

    pass


class _SubCNumpyImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="SubC",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """SubC Function -- Numpy implementation."""

    pass


class _SubCSelectorImpl(
    metaclass=_selector.Selector,
    ipps_class=_SubCIPPSImpl,
    numpy_class=_SubCNumpyImpl,
    numpy_types_L2=(_numpy.int32,),
):
    """SubC Function -- IPPS/Numpy selector."""

    pass


class _SubCIIPPSImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubC_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """SubC_I Function -- Intel IPPS implementation."""

    pass


class _SubCINumpyImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubC_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """SubC_I Function -- Numpy implementation."""

    pass


class _SubCSelectorImpl_I(
    metaclass=_selector.Selector,
    ipps_class=_SubCIIPPSImpl,
    numpy_class=_SubCINumpyImpl,
):
    """SubC_I Function -- IPPS/Numpy selector."""

    pass


class _SubCRevIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="SubCRev",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """SubCRev Function -- Intel IPPS implementation."""

    pass


class _SubCRevNumpyImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="SubCRev",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
    force_numpy=True,
):
    """SubCRev Function -- Numpy implementation."""

    pass


class _SubCRevSelectorImpl(
    metaclass=_selector.Selector,
    ipps_class=_SubCRevIPPSImpl,
    numpy_class=_SubCRevNumpyImpl,
    numpy_types_L2=(_numpy.int32,),
):
    """SubCRev Function -- IPPS/Numpy selector."""

    pass


class _SubCRevIIPPSImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubCRev_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """SubCRev_I Function -- Intel IPPS implementation."""

    pass


class _SubCRevINumpyImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubCRev_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
    force_numpy=True,
):
    """SubCRev_I Function -- Numpy implementation."""

    pass


class _SubCRevSelectorImpl_I(
    metaclass=_selector.Selector,
    ipps_class=_SubCRevIIPPSImpl,
    numpy_class=_SubCRevINumpyImpl,
):
    """SubCRev_I Function -- IPPS/Numpy selector."""

    pass


def SubC(size, dtype, polarity=Polarity.NORMAL):
    """SubC Function.

    Polarity.NORMAL  :  ``dst[n]  <-  src[n] - value``
    Polarity.REVERSE :  ``dst[n]  <-  value - src[n]``
    """
    if polarity is Polarity.NORMAL:
        return _SubCSelectorImpl(dtype=dtype, size=size)
    elif polarity is Polarity.REVERSE:
        return _SubCRevSelectorImpl(dtype=dtype, size=size)
    else:
        raise RuntimeError("Unknown polarity.")


SubC.dtype_candidates = _SubCIPPSImpl.dtype_candidates
SubC.__call__ = _SubCIPPSImpl.__call__


def SubC_I(size, dtype, polarity=Polarity.NORMAL):
    """SubC_I Function.

    Polarity.NORMAL  :  ``src_dst[n]  <-  src_dst[n] - value``
    Polarity.REVERSE :  ``src_dst[n]  <-  value - src_dst[n]``
    """
    if polarity is Polarity.NORMAL:
        return _SubCSelectorImpl_I(dtype=dtype, size=size)
    elif polarity is Polarity.REVERSE:
        return _SubCRevSelectorImpl_I(dtype=dtype, size=size)
    else:
        raise RuntimeError("Unknown polarity.")


SubC_I.dtype_candidates = _SubCIIPPSImpl.dtype_candidates
SubC_I.__call__ = _SubCIIPPSImpl.__call__


class _DivCIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="DivC",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=(
        _numpy.uint16,
        _numpy.float32,
    ),
):
    """DivC Function -- Intel IPPS implementation."""

    pass


class _DivCIPPSImpl_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="DivC_I",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=(
        _numpy.uint16,
        _numpy.float32,
    ),
):
    """DivC_I Function -- Intel IPPS implementation."""

    pass


class _DivCRevIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="DivCRev",
    numpy_backend=_numpy.divide,
    candidates=(
        _numpy.uint16,
        _numpy.float32,
    ),
    numpy_swap=True,
):
    """DivCRev Function -- Intel IPPS implementation."""

    pass


class _DivCRevNumpyImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="DivCRev",
    numpy_backend=_numpy.divide,
    candidates=(
        _numpy.uint16,
        _numpy.float32,
    ),
    numpy_swap=True,
    force_numpy=True,
):
    """DivCRev Function -- Numpy implementation."""

    pass


class _DivCRevSelectorImpl(
    metaclass=_selector.Selector,
    ipps_class=_DivCRevIPPSImpl,
    numpy_class=_DivCRevNumpyImpl,
    numpy_types_L2=(_numpy.float32,),
):
    """DivCRev Function -- IPPS/Numpy selector."""

    pass


class _DivCRevIPPSImpl_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="DivCRev_I",
    numpy_backend=_numpy.divide,
    candidates=(
        _numpy.uint16,
        _numpy.float32,
    ),
    numpy_swap=True,
):
    """DivCRev_I Function -- Intel IPPS  implementation."""

    pass


class _DivCRevNumpyImpl_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="DivCRev_I",
    numpy_backend=_numpy.divide,
    candidates=(
        _numpy.uint16,
        _numpy.float32,
    ),
    numpy_swap=True,
    force_numpy=True,
):
    """DivCRev_I Function -- Numpy implementation."""

    pass


class _DivCRevSelectorImpl_I(
    metaclass=_selector.Selector,
    ipps_class=_DivCRevIPPSImpl_I,
    numpy_class=_DivCRevNumpyImpl_I,
    numpy_types_L2=(_numpy.float32,),
):
    """DivCRev_I Function -- IPPS/Numpy selector."""

    pass


def DivC(size, dtype, polarity=Polarity.NORMAL):
    """DivC Function.

    Polarity.NORMAL  :  ``dst[n]  <-  src[n] / value``
    Polarity.REVERSE :  ``dst[n]  <-  value / src[n]``
    """
    if polarity is Polarity.NORMAL:
        return _DivCIPPSImpl(dtype=dtype, size=size)
    elif polarity is Polarity.REVERSE:
        return _DivCRevSelectorImpl(dtype=dtype, size=size)
    else:
        raise RuntimeError("Unknown polarity.")


DivC.dtype_candidates = _DivCIPPSImpl.dtype_candidates
DivC.__call__ = _DivCIPPSImpl.__call__


def DivC_I(size, dtype, polarity=Polarity.NORMAL):
    """DivC_I Function.

    Polarity.NORMAL  :  ``src_dst[n]  <-  src_dst[n] / value``
    Polarity.REVERSE :  ``src_dst[n]  <-  value / src_dst[n]``
    """
    if polarity is Polarity.NORMAL:
        return _DivCIPPSImpl_I(dtype=dtype, size=size)
    elif polarity is Polarity.REVERSE:
        return _DivCRevSelectorImpl_I(dtype=dtype, size=size)
    else:
        raise RuntimeError("Unknown polarity.")


DivC_I.dtype_candidates = _DivCIPPSImpl_I.dtype_candidates
DivC_I.__call__ = _DivCIPPSImpl_I.__call__
