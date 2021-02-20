"""FilterMedian Functions."""
import logging as _logging

import numpy as _numpy
import scipy.ndimage as _ndimage

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps.policies
import numpy_ipps.utils


class FilterMedian:
    """FilterMedian Function."""

    __slots__ = (
        "_ipps_backend",
        "_ipps_mask_size",
        "_ipps_dlySrc",
        "_ipps_dlyDst",
        "_ipps_mem_buffer",
        "_numpy_shift",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, continuous=False):
        self._ipps_mask_size = numpy_ipps.utils.cast("int", 2 * size + 1)
        self._numpy_shift = size

        if dtype == _numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif dtype == _numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        else:
            raise RuntimeError("Unknown dtype {}".format(dtype))

        if continuous:
            self._ipps_dlySrc = numpy_ipps.utils.ndarray(
                _numpy.zeros(2 * size, dtype=dtype)
            )
            self._ipps_dlyDst = numpy_ipps.utils.ndarray(
                _numpy.empty(2 * size, dtype=dtype)
            )
        else:
            self._ipps_dlySrc = numpy_ipps.utils.ndarray()
            self._ipps_dlyDst = numpy_ipps.utils.ndarray()

        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_median_getsize = _dispatch.ipps_function(
            "FilterMedianGetBufferSize",
            (
                "int",
                "int",
                "int*",
            ),
        )

        numpy_ipps.status = ipps_median_getsize(
            self._ipps_mask_size,
            ipps_type,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get FilterMedian size", name=__name__
        )

        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "FilterMedian allocations: working buffer {}o.".format(
                ipps_buffer_size[0]
            )
        )

        self._ipps_backend = _dispatch.ipps_function(
            "FilterMedian",
            (
                "void*",
                "void*",
                "int",
                "int",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
            self._ipps_mask_size,
            self._ipps_dlySrc.cdata,
            self._ipps_dlyDst.cdata,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.utils.swap_ndarray(self._ipps_dlySrc, self._ipps_dlyDst)

    def _numpy_backend(self, src, dst):
        _ndimage.median_filter(
            src.ndarray,
            size=int(self._ipps_mask_size),
            output=dst.ndarray,
            mode="nearest",
            origin=self._numpy_shift,
        )


class FilterMedian_I:
    """FilterMedian_I Function."""

    __slots__ = (
        "_ipps_backend",
        "_ipps_mask_size",
        "_ipps_dlySrc",
        "_ipps_dlyDst",
        "_ipps_mem_buffer",
        "_numpy_shift",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, size, dtype, continuous=False):
        self._ipps_mask_size = numpy_ipps.utils.cast("int", 2 * size + 1)
        self._numpy_shift = size

        if dtype == _numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif dtype == _numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        else:
            raise RuntimeError("Unknown dtype {}".format(dtype))

        if continuous:
            self._ipps_dlySrc = numpy_ipps.utils.ndarray(
                _numpy.zeros(2 * size, dtype=dtype)
            )
            self._ipps_dlyDst = numpy_ipps.utils.ndarray(
                _numpy.empty(2 * size, dtype=dtype)
            )
        else:
            self._ipps_dlySrc = numpy_ipps.utils.ndarray()
            self._ipps_dlyDst = numpy_ipps.utils.ndarray()

        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_median_getsize = _dispatch.ipps_function(
            "FilterMedianGetBufferSize",
            (
                "int",
                "int",
                "int*",
            ),
        )

        numpy_ipps.status = ipps_median_getsize(
            self._ipps_mask_size,
            ipps_type,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get FilterMedian size", name=__name__
        )

        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "FilterMedian allocations: working buffer {}o.".format(
                ipps_buffer_size[0]
            )
        )

        self._ipps_backend = _dispatch.ipps_function(
            "FilterMedian_I",
            (
                "void*",
                "int",
                "int",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self._ipps_backend(
            src_dst.cdata,
            src_dst.size,
            self._ipps_mask_size,
            self._ipps_dlySrc.cdata,
            self._ipps_dlyDst.cdata,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.utils.swap_ndarray(self._ipps_dlySrc, self._ipps_dlyDst)

    def _numpy_backend(self, src_dst):
        _ndimage.median_filter(
            src_dst.ndarray,
            size=int(self._ipps_mask_size),
            output=src_dst.ndarray,
            mode="nearest",
            origin=self._numpy_shift,
        )
