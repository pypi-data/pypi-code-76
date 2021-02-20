"""Arithmetic Integer Functions."""
import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps.policies
import numpy_ipps.utils


class SwapBytes:
    """SwapBytes Function."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = (
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
        _numpy.int64,
        _numpy.uint64,
        _numpy.float32,
        _numpy.float64,
    )
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "SwapBytes",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.Policies(
                bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes4=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes8=numpy_ipps.policies.TagPolicy.UNSIGNED,
            ),
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, src.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = src.ndarray.byteswap()


class SwapBytes_I:
    """SwapBytes_I Function."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = (
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
        _numpy.int64,
        _numpy.uint64,
        _numpy.float32,
        _numpy.float64,
    )
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "SwapBytes_I",
            (
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.Policies(
                bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes4=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes8=numpy_ipps.policies.TagPolicy.UNSIGNED,
            ),
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self._ipps_backend(src_dst.cdata, src_dst.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src_dst):
        src_dst.ndarray[:] = src_dst.ndarray.byteswap(True)


class Flip:
    """Flip Function."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.default_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Flip",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.Policies(
                bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes4=numpy_ipps.policies.TagPolicy.FLOAT,
                bytes8=numpy_ipps.policies.TagPolicy.FLOAT,
            ),
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, src.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _numpy.flip(src.ndarray)


class Flip_I:
    """Flip_I Function."""

    __slots__ = ("_ipps_backend",)
    dtype_candidates = numpy_ipps.policies.default_candidates
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Flip_I",
            (
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.Policies(
                bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes4=numpy_ipps.policies.TagPolicy.FLOAT,
                bytes8=numpy_ipps.policies.TagPolicy.FLOAT,
            ),
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self._ipps_backend(src_dst.cdata, src_dst.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src_dst):
        src_dst.ndarray[:] = _numpy.flip(src_dst.ndarray)


class Convert:
    """Conver Function."""

    __slots__ = (
        "_ipps_backend",
        "_dst_dtype",
    )
    dtype_candidates = (
        (_numpy.int8, _numpy.int16),
        (_numpy.int8, _numpy.float32),
        (_numpy.uint8, _numpy.float32),
        (_numpy.int16, _numpy.int32),
        (_numpy.int16, _numpy.float32),
        (_numpy.uint16, _numpy.float32),
        (_numpy.int32, _numpy.float64),
        (_numpy.float32, _numpy.float64),
    )
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype_src, dtype_dst, size=None):
        self._dst_dtype = dtype_dst
        self._ipps_backend = _dispatch.ipps_function(
            "Convert",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype_src,
            dtype_dst,
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, src.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = src.ndarray.astype(self._dst_dtype, casting="unsafe")


class Threshold:
    """Threshold Function."""

    __slots__ = (
        "_ipps_backend",
        "_ipps_level",
        "_dtype",
        "_ge_buffer",
    )
    dtype_candidates = (
        _numpy.int16,
        _numpy.int32,
        _numpy.float32,
        _numpy.float64,
    )
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype, level, size=None):
        self._dtype = dtype
        self._ipps_level = numpy_ipps.utils.cast(
            _dispatch.as_ctype_str(dtype), level
        )
        self._ipps_backend = _dispatch.ipps_function(
            "Threshold-LTAbs",
            (
                "void*",
                "void*",
                "int",
                _dispatch.as_ctype_str(dtype),
            ),
            dtype,
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src.cdata, dst.cdata, src.size, self._ipps_level
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        _numpy.absolute(src.ndarray, dst.ndarray, casting="unsafe")
        dst.ndarray[:] = _numpy.where(
            dst.ndarray >= self._dtype(self._ipps_level),
            src.ndarray,
            _numpy.sign(src.ndarray, casting="unsafe")
            * self._dtype(self._ipps_level),
        )


class Threshold_I:
    """Threshold Function."""

    __slots__ = (
        "_ipps_backend",
        "_ipps_level",
        "_dtype",
    )
    dtype_candidates = (
        _numpy.int16,
        _numpy.int32,
        _numpy.float32,
        _numpy.float64,
    )
    _ipps_kind = _selector.Kind.UNARY_I

    def __init__(self, dtype, level, size=None):
        self._dtype = dtype
        self._ipps_level = numpy_ipps.utils.cast(
            _dispatch.as_ctype_str(dtype), level
        )
        self._ipps_backend = _dispatch.ipps_function(
            "Threshold-LTAbs_I",
            (
                "void*",
                "int",
                _dispatch.as_ctype_str(dtype),
            ),
            dtype,
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self._ipps_backend(
            src_dst.cdata, src_dst.size, self._ipps_level
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src_dst):
        src_dst.ndarray[:] = _numpy.where(
            _numpy.absolute(src_dst.ndarray, casting="unsafe")
            >= self._dtype(self._ipps_level),
            src_dst.ndarray,
            _numpy.sign(src_dst.ndarray, casting="unsafe")
            * self._dtype(self._ipps_level),
        )
