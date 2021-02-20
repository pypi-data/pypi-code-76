"""Fast Fourier Transform Functions."""
import logging as _logging

import numpy as _numpy
import scipy.fftpack as _fft

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.libipp as _libipp
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps.policies
import numpy_ipps.utils


class FFTFwd:
    """FFT forward Function.

    ``dst  <-  FFT[ src ]``
    """

    __slots__ = (
        "_ipps_backend",
        "_numpy_callback",
        "_ipps_spec",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
    )
    dtype_candidates = numpy_ipps.policies.float_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, order, dtype):
        ipps_flag = numpy_ipps.utils.cast("int", 2)

        self._ipps_spec = numpy_ipps.utils.new("void**")

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_spec_buffer_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "FFTGetSize-{}".format(
                "C" if dtype in numpy_ipps.policies.complex_candidates else "R"
            ),
            (
                "int",
                "int",
                "IppHintAlgorithm",
                "int*",
                "int*",
                "int*",
            ),
            dtype,
        )
        ipps_fft_init = _dispatch.ipps_function(
            "FFTInit-{}".format(
                "C" if dtype in numpy_ipps.policies.complex_candidates else "R"
            ),
            (
                "void**",
                "int",
                "int",
                "IppHintAlgorithm",
                "void*",
                "void*",
            ),
            dtype,
        )

        numpy_ipps.status = ipps_fft_getsize(
            order,
            ipps_flag,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            ipps_spec_size,
            ipps_spec_buffer_size,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get FFT size", name=__name__
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_size[0], dtype=_numpy.uint8)
        )
        ipps_mem_init = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_buffer_size[0], dtype=_numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "FFT allocations: spec {}o -- buffer {}o.".format(
                ipps_spec_size[0], ipps_buffer_size[0]
            )
        )

        numpy_ipps.status = ipps_fft_init(
            self._ipps_spec,
            order,
            ipps_flag,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            self._ipps_mem_spec.cdata,
            ipps_mem_init.cdata,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Init FFT", name=__name__
        )

        self._ipps_backend = _dispatch.ipps_function(
            "FFTFwd-{}".format(
                "CToC"
                if dtype in numpy_ipps.policies.complex_candidates
                else "RToPerm"
            ),
            (
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )

        self._numpy_callback = (
            _fft.fft
            if dtype in numpy_ipps.policies.complex_candidates
            else _fft.rfft
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = self._numpy_callback(src.ndarray)


class FFTInv:
    """FFT inverse Function.

    ``dst  <-  iFFT[ src ]``
    """

    __slots__ = (
        "_ipps_backend",
        "_numpy_callback",
        "_ipps_spec",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
    )
    dtype_candidates = numpy_ipps.policies.float_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, order, dtype):
        ipps_flag = numpy_ipps.utils.cast("int", 2)

        self._ipps_spec = numpy_ipps.utils.new("void**")

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_spec_buffer_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "FFTGetSize-{}".format(
                "C" if dtype in numpy_ipps.policies.complex_candidates else "R"
            ),
            (
                "int",
                "int",
                "IppHintAlgorithm",
                "int*",
                "int*",
                "int*",
            ),
            dtype,
        )
        ipps_fft_init = _dispatch.ipps_function(
            "FFTInit-{}".format(
                "C" if dtype in numpy_ipps.policies.complex_candidates else "R"
            ),
            (
                "void**",
                "int",
                "int",
                "IppHintAlgorithm",
                "void*",
                "void*",
            ),
            dtype,
        )

        numpy_ipps.status = ipps_fft_getsize(
            order,
            ipps_flag,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            ipps_spec_size,
            ipps_spec_buffer_size,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get FFT size", name=__name__
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_size[0], dtype=_numpy.uint8)
        )
        ipps_mem_init = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_buffer_size[0], dtype=_numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "FFT allocations: spec {}o -- buffer {}o.".format(
                ipps_spec_size[0], ipps_buffer_size[0]
            )
        )

        numpy_ipps.status = ipps_fft_init(
            self._ipps_spec,
            order,
            ipps_flag,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            self._ipps_mem_spec.cdata,
            ipps_mem_init.cdata,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Init FFT", name=__name__
        )

        self._ipps_backend = _dispatch.ipps_function(
            "FFTInv-{}".format(
                "CToC"
                if dtype in numpy_ipps.policies.complex_candidates
                else "PermToR"
            ),
            (
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )

        self._numpy_callback = (
            _fft.ifft
            if dtype in numpy_ipps.policies.complex_candidates
            else _fft.irfft
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = self._numpy_callback(src.ndarray)
