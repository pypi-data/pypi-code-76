"""Signal Functions."""
import enum as _enum
import logging as _logging

import numpy as _numpy
import scipy.signal as _signal

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.utils


class ConjPerm(
    metaclass=_unaries.Unary,
    ipps_backend="ConjPerm",
    candidates=numpy_ipps.policies.complex_candidates,
):
    """ConjPerm Function."""

    pass


class ConjPerm_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="ConjPerm_I",
    candidates=numpy_ipps.policies.complex_candidates,
):
    """ConjPerm_I Function."""

    pass


class Method(_enum.Enum):
    """Method enumeration."""

    DIRECT = 1
    FFT = 2


class Convolve:
    """Convolve Function.

    ``dst  <-  src1 conv src2``
    """

    __slots__ = (
        "_ipps_backend",
        "_ipps_mem_buffer",
        "_ipps_method",
        "_numpy_method",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, size, dtype, method=Method.DIRECT):
        if method is Method.DIRECT:
            self._ipps_method = numpy_ipps.utils.cast("int", 0x00000001)
            self._numpy_method = "direct"
        elif method is Method.FFT:
            self._ipps_method = numpy_ipps.utils.cast("int", 0x00000002)
            self._numpy_method = "fft"
        else:
            raise RuntimeError("Unknown method {}".format(method))

        if dtype == _numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif dtype == _numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        else:
            raise RuntimeError(
                "Unknown dtype {}".format(self._ipps_kernel.ndarray.dtype)
            )

        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "ConvolveGetBufferSize",
            (
                "int",
                "int",
                "int",
                "int",
                "int*",
            ),
        )

        numpy_ipps.status = ipps_fft_getsize(
            size,
            size,
            ipps_type,
            self._ipps_method,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get Convolve size", name=__name__
        )

        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "Convolve allocations: working buffer {}o.".format(
                ipps_buffer_size[0]
            )
        )

        self._ipps_backend = _dispatch.ipps_function(
            "Convolve",
            (
                "void*",
                "int",
                "void*",
                "int",
                "void*",
                "int",
                "void*",
            ),
            dtype,
        )

    def __call__(self, src1, src2, dst):
        numpy_ipps.status = self._ipps_backend(
            src1.cdata,
            src1.size,
            src2.cdata,
            src2.size,
            dst.cdata,
            self._ipps_method,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src1, src2, dst):
        dst.ndarray[:] = _signal.convolve(
            src1.ndarray, src2.ndarray, mode="full", method=self._numpy_method
        )


class Correlate:
    """Correlate Function.

    ``dst  <-  src1 corr src2``
    """

    __slots__ = (
        "_ipps_backend",
        "_ipps_mem_buffer",
        "_ipps_method",
        "_ipps_lag",
        "_numpy_method",
    )
    dtype_candidates = numpy_ipps.policies.float_candidates
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, size, dtype, method=Method.DIRECT):
        if method is Method.DIRECT:
            self._ipps_method = numpy_ipps.utils.cast("int", 0x00000001)
            self._numpy_method = "direct"
        elif method is Method.FFT:
            self._ipps_method = numpy_ipps.utils.cast("int", 0x00000002)
            self._numpy_method = "fft"
        else:
            raise RuntimeError("Unknown method {}".format(method))

        if dtype == _numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif dtype == _numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        elif dtype == _numpy.complex64:
            ipps_type = numpy_ipps.utils.cast("int", 14)
        elif dtype == _numpy.complex128:
            ipps_type = numpy_ipps.utils.cast("int", 20)
        else:
            raise RuntimeError(
                "Unknown dtype {}".format(self._ipps_kernel.ndarray.dtype)
            )

        self._ipps_lag = numpy_ipps.utils.cast("int", -(size >> 1))

        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "CrossCorrNormGetBufferSize",
            (
                "int",
                "int",
                "int",
                "int",
                "int",
                "int",
                "int*",
            ),
        )

        numpy_ipps.status = ipps_fft_getsize(
            size,
            size,
            size,
            self._ipps_lag,
            ipps_type,
            self._ipps_method,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get Correlate size", name=__name__
        )

        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "Correlate allocations: working buffer {}o.".format(
                ipps_buffer_size[0]
            )
        )

        self._ipps_backend = _dispatch.ipps_function(
            "CrossCorrNorm",
            (
                "void*",
                "int",
                "void*",
                "int",
                "void*",
                "int",
                "int",
                "int",
                "void*",
            ),
            dtype,
        )

    def __call__(self, src1, src2, dst):
        assert src1.size == dst.size, "src1 and dst size not compatible."
        assert src2.size == dst.size, "src2 and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src1.cdata,
            src1.size,
            src2.cdata,
            src2.size,
            dst.cdata,
            dst.size,
            self._ipps_lag,
            self._ipps_method,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src1, src2, dst):
        assert src1.size == dst.size, "src1 and dst size not compatible."
        assert src2.size == dst.size, "src2 and dst size not compatible."

        dst.ndarray[:] = _signal.correlate(
            src2.ndarray, src1.ndarray, mode="same", method=self._numpy_method
        )


class AutoCorrelate:
    """Auto Correlate Function.

    ``dst  <-  src corr src``
    """

    __slots__ = (
        "_ipps_backend",
        "_ipps_mem_buffer",
        "_ipps_method",
        "_numpy_method",
    )
    dtype_candidates = numpy_ipps.policies.float_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, method=Method.DIRECT):
        if method is Method.DIRECT:
            self._ipps_method = numpy_ipps.utils.cast("int", 0x00000001)
            self._numpy_method = "direct"
        elif method is Method.FFT:
            self._ipps_method = numpy_ipps.utils.cast("int", 0x00000002)
            self._numpy_method = "fft"
        else:
            raise RuntimeError("Unknown method {}".format(method))

        if dtype == _numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif dtype == _numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        elif dtype == _numpy.complex64:
            ipps_type = numpy_ipps.utils.cast("int", 14)
        elif dtype == _numpy.complex128:
            ipps_type = numpy_ipps.utils.cast("int", 20)
        else:
            raise RuntimeError(
                "Unknown dtype {}".format(self._ipps_kernel.ndarray.dtype)
            )

        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "AutoCorrNormGetBufferSize",
            (
                "int",
                "int",
                "int",
                "int",
                "int*",
            ),
        )

        numpy_ipps.status = ipps_fft_getsize(
            size,
            size,
            ipps_type,
            self._ipps_method,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get Correlate size", name=__name__
        )

        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "Correlate allocations: working buffer {}o.".format(
                ipps_buffer_size[0]
            )
        )

        self._ipps_backend = _dispatch.ipps_function(
            "AutoCorrNorm",
            (
                "void*",
                "int",
                "void*",
                "int",
                "int",
                "void*",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        assert src.size == dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            src.size,
            dst.cdata,
            dst.size,
            self._ipps_method,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        assert src.size == dst.size, "src and dst size not compatible."

        dst.ndarray[:] = _signal.correlate(
            src.ndarray, src.ndarray, mode="full", method=self._numpy_method
        )[-int(src.size) :]
