"""Vector Initialization Functions."""
import enum as _enum

import numpy as _numpy

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


_init_policies = numpy_ipps.policies.Policies(
    bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
    bytes2=numpy_ipps.policies.TagPolicy.SIGNED,
    bytes4=numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
    bytes8=numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
)


class Assign:
    """Assign Function.

    ``dst[n]  <-  src[n]``
    """

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.default_candidates
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype, overlap=False):
        if overlap:
            self._ipps_backend = _dispatch.ipps_function(
                "Move",
                (
                    "void*",
                    "void*",
                    "int",
                ),
                dtype,
                policies=_init_policies,
            )
        else:
            self._ipps_backend = _dispatch.ipps_function(
                "Copy",
                (
                    "void*",
                    "void*",
                    "int",
                ),
                dtype,
                policies=_init_policies,
            )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, src.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        _numpy.copyto(dst.ndarray[: int(src.size)], src.ndarray)


class Endian(_enum.Enum):
    """Endianess Enum."""

    LITTLE = 1
    BIG = 2


class BitShift:
    """BitShift Function."""

    __slots__ = (
        "_ipps_backend",
        "src_bit_offset",
        "dst_bit_offset",
    )
    dtype_candidates = (_numpy.uint8,)
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(
        self,
        src_bit_offset=0,
        dst_bit_offset=0,
        endian=Endian.LITTLE,
    ):
        self.src_bit_offset = numpy_ipps.utils.cast("int", src_bit_offset)
        self.dst_bit_offset = numpy_ipps.utils.cast("int", dst_bit_offset)

        if endian == Endian.LITTLE:
            self._ipps_backend = _dispatch.ipps_function(
                "CopyLE-1u",
                (
                    "void*",
                    "int",
                    "void*",
                    "int",
                    "int",
                ),
            )
        elif endian == Endian.BIG:
            self._ipps_backend = _dispatch.ipps_function(
                "CopyBE-1u",
                (
                    "void*",
                    "int",
                    "void*",
                    "int",
                    "int",
                ),
            )
        else:
            _debug.log_and_raise(
                RuntimeError,
                "Unknown endianess: {}".format(endian),
                name=__name__,
            )

    def __call__(self, src, dst, size):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            self.src_bit_offset,
            dst.cdata,
            self.dst_bit_offset,
            size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class _SetToIPPSImpl:
    """SetTo Function -- Intel IPPS implementation."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = (
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
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Set",
            (
                _dispatch.as_ctype_str(dtype, policies=_init_policies),
                "void*",
                "int",
            ),
            dtype,
            policies=_init_policies,
        )

    def __call__(self, dst, value):
        numpy_ipps.status = self._ipps_backend(value, dst.cdata, dst.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, dst, value):
        dst.ndarray[:] = value


class _SetToNumpyImpl:
    """SetTo Function -- Numpy implementation."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = (
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
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Set",
            (
                _dispatch.as_ctype_str(dtype, policies=_init_policies),
                "void*",
                "int",
            ),
            dtype,
            policies=_init_policies,
        )

    def __call__(self, dst, value):
        dst.ndarray[:] = value

    def _numpy_backend(self, dst, value):
        dst.ndarray[:] = value


class SetTo(
    metaclass=_selector.Selector,
    ipps_class=_SetToIPPSImpl,
    numpy_class=_SetToNumpyImpl,
    numpy_types_L2=(
        _numpy.uint16,
        _numpy.int16,
    ),
):
    """SetTo Function.

    ``dst[n]  <-  value``
    """

    pass


class Zeros:
    """Zeros Function.

    ``dst[n]  <-  0``
    """

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.default_candidates
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype):
        self._ipps_backend = _dispatch.ipps_function(
            "Zero",
            (
                "void*",
                "int",
            ),
            dtype,
            policies=_init_policies,
        )

    def __call__(self, dst):
        numpy_ipps.status = self._ipps_backend(dst.cdata, dst.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, dst):
        dst.ndarray[:] = 0
