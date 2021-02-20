"""IIR Functions."""
import logging as _logging

import numpy as _numpy

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps.policies
import numpy_ipps.utils


class IIR:
    """IIR Function."""

    __slots__ = (
        "_ipps_backend",
        "_ipps_dlySrc",
        "_ipps_dlyDst",
        "_ipps_mem_buffer",
        "_ipps_state",
    )
    dtype_candidates = numpy_ipps.policies.float_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, kernel, biquad=False):
        self._ipps_state = numpy_ipps.utils.new("void**")
        ipps_kernel = numpy_ipps.utils.ndarray(kernel)

        if biquad:
            ipps_order = int(ipps_kernel.size) // 6
        else:
            ipps_order = (int(ipps_kernel.size) >> 1) - 1
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_iir_getsize = _dispatch.ipps_function(
            "IIRGetStateSize{}".format("-BiQuad" if biquad else ""),
            (
                "int",
                "int*",
            ),
            kernel.dtype,
        )
        ipps_iir_init = _dispatch.ipps_function(
            "IIRInit{}".format("-BiQuad" if biquad else ""),
            (
                "void*",
                "void*",
                "int",
                "void*",
                "void*",
            ),
            kernel.dtype,
        )

        numpy_ipps.status = ipps_iir_getsize(
            ipps_order,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get IIR size", name=__name__
        )

        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "IIR allocations: working buffer {}o.".format(ipps_buffer_size[0])
        )

        _ipps_dlySrc = numpy_ipps.utils.ndarray()

        numpy_ipps.status = ipps_iir_init(
            self._ipps_state,
            ipps_kernel.cdata,
            ipps_order,
            _ipps_dlySrc.cdata,
            self._ipps_mem_buffer.cdata,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Init IIR", name=__name__
        )

        self._ipps_backend = _dispatch.ipps_function(
            "IIR",
            (
                "void*",
                "void*",
                "int",
                "void*",
            ),
            kernel.dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
            self._ipps_state[0],
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class IIR_I:
    """IIR_I Function."""

    __slots__ = (
        "_ipps_backend",
        "_ipps_dlySrc",
        "_ipps_dlyDst",
        "_ipps_mem_buffer",
        "_ipps_state",
    )
    dtype_candidates = numpy_ipps.policies.float_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, kernel, biquad=False):
        self._ipps_state = numpy_ipps.utils.new("void**")
        ipps_kernel = numpy_ipps.utils.ndarray(kernel)

        if biquad:
            ipps_order = int(ipps_kernel.size) // 6
        else:
            ipps_order = (int(ipps_kernel.size) >> 1) - 1
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_iir_getsize = _dispatch.ipps_function(
            "IIRGetStateSize{}".format("-BiQuad" if biquad else ""),
            (
                "int",
                "int*",
            ),
            kernel.dtype,
        )
        ipps_iir_init = _dispatch.ipps_function(
            "IIRInit{}".format("-BiQuad" if biquad else ""),
            (
                "void*",
                "void*",
                "int",
                "void*",
                "void*",
            ),
            kernel.dtype,
        )

        numpy_ipps.status = ipps_iir_getsize(
            ipps_order,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get IIR size", name=__name__
        )

        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "IIR allocations: working buffer {}o.".format(ipps_buffer_size[0])
        )

        _ipps_dlySrc = numpy_ipps.utils.ndarray()

        numpy_ipps.status = ipps_iir_init(
            self._ipps_state,
            ipps_kernel.cdata,
            ipps_order,
            _ipps_dlySrc.cdata,
            self._ipps_mem_buffer.cdata,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Init IIR", name=__name__
        )

        self._ipps_backend = _dispatch.ipps_function(
            "IIR_I",
            (
                "void*",
                "int",
                "void*",
            ),
            kernel.dtype,
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self._ipps_backend(
            src_dst.cdata,
            src_dst.size,
            self._ipps_state[0],
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src_dst):
        raise NotImplementedError
