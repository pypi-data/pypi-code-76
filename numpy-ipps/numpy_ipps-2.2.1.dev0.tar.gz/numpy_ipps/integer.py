"""Arithmetic Integer Functions."""
import enum as _enum

import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


_binaryInt_candidates = (
    _numpy.uint8,
    _numpy.int16,
    _numpy.uint16,
    _numpy.int32,
)
_unarySignedInt_candidates = (
    _numpy.int16,
    _numpy.int32,
)
_unaryUnsignedInt_candidates = (
    _numpy.uint8,
    _numpy.int16,
    _numpy.uint16,
)


class Polarity(_enum.Enum):
    """Polarity enumeration."""

    NORMAL = 1
    REVERSE = 2


class AddInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Add",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes4=numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
        bytes8=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
    ),
    candidates=(
        _numpy.int8,
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
    ),
):
    """Add Function.

    ``dst[n]  <-  src1[n] + src2[n]``
    """

    pass


class AddInteger_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Add_I",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SIGNED,
        bytes4=numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
    ),
    candidates=(
        _numpy.int8,
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
    ),
):
    """Add_I Function.

    ``src_dst[n]  <-  src_dst[n] + src[n]``
    """

    pass


class _MulIntegerIPPSImpl(
    metaclass=_binaries.Binary,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """Mul Function -- Intel IPPS implementation."""

    pass


class _MulIntegerNumpyImpl(
    metaclass=_binaries.Binary,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """Mul Function -- Numpy implementation."""

    pass


class MulInteger(
    metaclass=_selector.Selector,
    ipps_class=_MulIntegerIPPSImpl,
    numpy_class=_MulIntegerNumpyImpl,
    numpy_types_L2=(_numpy.int32,),
):
    """Mul Function.

    ``dst[n]  <-  src1[n] * src2[n]``
    """

    pass


class _MulIntegerIIPPSImpl(
    metaclass=_binaries.Binary_I,
    ipps_backend="Mul_I",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """Mul_I Function -- Intel IPPS implementation."""

    pass


class _MulIntegerINumpyImpl(
    metaclass=_binaries.Binary_I,
    ipps_backend="Mul_I",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """Mul_I Function -- Numpy implementation."""

    pass


class MulInteger_I(
    metaclass=_selector.Selector,
    ipps_class=_MulIntegerIIPPSImpl,
    numpy_class=_MulIntegerINumpyImpl,
    numpy_types_L2=(_numpy.int32,),
):
    """Mul_I Function.

    ``src_dst[n]  <-  src_dst[n] * src[n]``
    """

    pass


class SubInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """Sub Function.

    ``dst[n]  <-  src2[n] - src1[n]``
    """

    pass


class SubInteger_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Sub_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """Sub_I Function.

    ``src_dst[n]  <-  src[n] - src_dst[n]``
    """

    pass


class DivInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """Div Function.

    dst[n]  <-  src2[n] / src1[n]
    """

    pass


class DivInteger_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Div_I",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=(
        _numpy.int16,
        _numpy.uint16,
    ),
    numpy_swap=True,
):
    """Div_I Function.

    ``src_dst[n]  <-  src[n] / src_dst[n]``
    """

    pass


class AbsInteger(
    metaclass=_unaries.Unary,
    ipps_backend="Abs",
    numpy_backend=_numpy.fabs,
    candidates=_unarySignedInt_candidates,
):
    """Abs Function.

    ``dst[n]  <-  | src[n] |``
    """

    pass


class AbsInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Abs_I",
    numpy_backend=_numpy.fabs,
    candidates=_unarySignedInt_candidates,
):
    """Abs_I Function.

    ``src_dst[n]  <-  | src_dst[n] |``
    """

    pass


class _SqrIntegerIPPSImpl(
    metaclass=_unaries.Unary,
    ipps_backend="Sqr",
    numpy_backend=_numpy.square,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
):
    """Sqr Function -- Intel IPPS implementation."""

    pass


class _SqrIntegerNumpyImpl(
    metaclass=_unaries.Unary,
    ipps_backend="Sqr",
    numpy_backend=_numpy.square,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
    force_numpy=True,
):
    """Sqr Function -- Numpy implementation."""

    pass


class SqrInteger(
    metaclass=_selector.Selector,
    ipps_class=_SqrIntegerIPPSImpl,
    numpy_class=_SqrIntegerNumpyImpl,
    numpy_types_L2=(
        _numpy.int16,
        _numpy.uint16,
    ),
):
    """Sqr Function.

    ``dst[n]  <-  src[n] * src[n]``
    """

    pass


class SqrInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Sqr_I",
    numpy_backend=_numpy.square,
    policies=numpy_ipps.policies.scaled_all,
    candidates=(_numpy.uint8,),
):
    """Sqr_I Function.

    ``src_dst[n]  <-  src_dst[n] * src_dst[n]``
    """

    pass


class SqrtInteger(
    metaclass=_unaries.Unary,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
):
    """Sqrt Function.

    ``dst[n]  <-  sqrt( src[n] )``
    """

    pass


class SqrtInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Sqrt_I",
    numpy_backend=_numpy.sqrt,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
):
    """Sqrt_I Function.

    ``src_dst[n]  <-  sqrt( src_dst[n] )``
    """

    pass


class ExpInteger(
    metaclass=_unaries.Unary,
    ipps_backend="Exp",
    numpy_backend=_numpy.exp,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
):
    """Exp Function.

    ``dst[n]  <-  exp( src[n] )``
    """

    pass


class ExpInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Exp_I",
    numpy_backend=_numpy.exp,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
):
    """Exp_I Function.

    ``src_dst[n]  <-  exp( src_dst[n] )``
    """

    pass


class LnInteger(
    metaclass=_unaries.Unary,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
):
    """Ln Function.

    ``dst[n]  <-  ln( src[n] )``
    """

    pass


class LnInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Ln_I",
    numpy_backend=_numpy.log,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
):
    """Ln_I Function.

    ``src_dst[n]  <-  ln( src_dst[n] )``
    """

    pass


class AddProductInteger:
    """AddProduct Function.

    ``src_dst[n]  <-  src_dst[n]  +  src1[n] * src2[n]``
    """

    __slots__ = (
        "_ipps_backend",
        "_ipps_arg",
    )
    dtype_candidates = (
        _numpy.int16,
        _numpy.int32,
    )
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, dtype, size=None):
        self._ipps_arg = numpy_ipps.utils.cast("int", 0)

        self._ipps_backend = _dispatch.ipps_function(
            "AddProduct",
            (
                "void*",
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.scaled_all,
        )

    def __call__(self, src1, src2, src_dst):
        numpy_ipps.status = self._ipps_backend(
            src1.cdata,
            src2.cdata,
            src_dst.cdata,
            src1.size,
            self._ipps_arg,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src1, src2, src_dst):
        raise NotImplementedError


class NormalizeInteger:
    """Normalize Function.

    ``dst[n]  <-  (src[n] - sub) / div``
    """

    __slots__ = (
        "_ipps_backend",
        "_ipps_arg",
    )
    dtype_candidates = (_numpy.int16,)
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, size=None):
        self._ipps_arg = numpy_ipps.utils.cast("int", 0)

        self._ipps_backend = _dispatch.ipps_function(
            "Normalize",
            (
                "void*",
                "void*",
                "int",
                _dispatch.as_ctype_str(
                    dtype, policies=numpy_ipps.policies.scaled_all
                ),
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.scaled_all,
        )

    def __call__(self, src, dst, sub, div):
        numpy_ipps.status = self._ipps_backend(
            src.cdata, dst.cdata, src.size, sub, div, self._ipps_arg
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst, sub, div):
        _numpy.subtract(src.ndarray, sub, dst.ndarray, casting="unsafe")
        _numpy.divide(dst.ndarray, div, dst.ndarray, casting="unsafe")


class NormalizeInteger_I:
    """Normalize_I Function.

    ``src_dst[n]  <-  (src_dst[n] - sub) / div``
    """

    __slots__ = (
        "_ipps_backend",
        "_ipps_arg",
    )
    dtype_candidates = (_numpy.int16,)
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype, size=None):
        self._ipps_arg = numpy_ipps.utils.cast("int", 0)

        self._ipps_backend = _dispatch.ipps_function(
            "Normalize_I",
            (
                "void*",
                "int",
                _dispatch.as_ctype_str(
                    dtype, policies=numpy_ipps.policies.scaled_all
                ),
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.scaled_all,
        )

    def __call__(self, src_dst, sub, div):
        numpy_ipps.status = self._ipps_backend(
            src_dst.cdata, src_dst.size, sub, div, self._ipps_arg
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src_dst, sub, div):
        _numpy.subtract(
            src_dst.ndarray, sub, src_dst.ndarray, casting="unsafe"
        )
        _numpy.divide(src_dst.ndarray, div, src_dst.ndarray, casting="unsafe")
