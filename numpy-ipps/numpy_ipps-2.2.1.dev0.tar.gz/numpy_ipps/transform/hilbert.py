"""Fast Hilbert Transform Functions."""
import logging as _logging

import numpy as _numpy
import scipy.signal as _signal

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.libipp as _libipp
import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps.policies
import numpy_ipps.utils


class Hilbert:
    """Hilbert Function.

    ``dst  <-  Hilbert[ src ]``
    """

    __slots__ = (
        "_ipps_backend",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
    )
    dtype_candidates = numpy_ipps.policies.complex_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, order, dtype):
        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_hilbert_getsize = _dispatch.ipps_function(
            "HilbertGetSize",
            (
                "int",
                "IppHintAlgorithm",
                "int*",
                "int*",
            ),
            dtype().real.dtype.type,
            dtype,
        )
        ipps_hilbert_init = _dispatch.ipps_function(
            "HilbertInit",
            (
                "int",
                "IppHintAlgorithm",
                "void*",
                "void*",
            ),
            dtype().real.dtype.type,
            dtype,
        )

        numpy_ipps.status = ipps_hilbert_getsize(
            order,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            ipps_spec_size,
            ipps_buffer_size,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Get Hilbert size", name=__name__
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_size[0], dtype=_numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "Hilbert allocations: spec {}o -- buffer {}o.".format(
                ipps_spec_size[0], ipps_buffer_size[0]
            )
        )

        numpy_ipps.status = ipps_hilbert_init(
            order,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            self._ipps_mem_spec.cdata,
            self._ipps_mem_buffer.cdata,
        )
        _debug.assert_status(
            numpy_ipps.status, message="Init Hilbert", name=__name__
        )

        self._ipps_backend = _dispatch.ipps_function(
            "Hilbert",
            (
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype().real.dtype.type,
            dtype,
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            self._ipps_mem_spec.cdata,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _signal.hilbert(src.ndarray)
