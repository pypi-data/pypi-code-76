import numpy
import pytest

import numpy_ipps._detail.dispatch
import numpy_ipps._detail.libipp
import numpy_ipps.initialization
import numpy_ipps.logical
import numpy_ipps.utils


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))


class IPPSFirFFT:
    __slots__ = (
        "_ipps_backend_fft",
        "_ipps_backend_ifft",
        "_ipps_backend_mul",
        "_ipps_spec",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
        "_ipps_kernel",
        "_ipps_spectrum",
    )

    def __init__(self, kernel, order, dtype=numpy.complex128):
        ipps_flag = numpy_ipps.utils.cast("int", 2)

        self._ipps_spec = numpy_ipps.utils.new("void**")

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_spec_buffer_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = numpy_ipps._detail.dispatch.ipps_function(
            "FFTGetSize-C",
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
        ipps_fft_init = numpy_ipps._detail.dispatch.ipps_function(
            "FFTInit-C",
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
            numpy_ipps._detail.libipp.ffi.typeof("IppHintAlgorithm").relements[
                "ippAlgHintNone"
            ],
            ipps_spec_size,
            ipps_spec_buffer_size,
            ipps_buffer_size,
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_spec_size[0], dtype=numpy.uint8)
        )
        ipps_mem_init = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_spec_buffer_size[0], dtype=numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_buffer_size[0], dtype=numpy.uint8)
        )

        numpy_ipps.status = ipps_fft_init(
            self._ipps_spec,
            order,
            ipps_flag,
            numpy_ipps._detail.libipp.ffi.typeof("IppHintAlgorithm").relements[
                "ippAlgHintNone"
            ],
            self._ipps_mem_spec.cdata,
            ipps_mem_init.cdata,
        )

        self._ipps_backend_fft = numpy_ipps._detail.dispatch.ipps_function(
            "FFTFwd-CToC",
            (
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )
        self._ipps_backend_ifft = numpy_ipps._detail.dispatch.ipps_function(
            "FFTInv-CToC",
            (
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )

        self._ipps_backend_mul = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "Mul",
                dtype,
                numpy_ipps.policies.Accuracy.LEVEL_3,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

        kernel_pad = numpy_ipps.utils.ndarray(
            numpy.zeros(1 << order, dtype=dtype)
        )
        kernel_pad.ndarray[: kernel.size] = kernel.flatten()
        self._ipps_kernel = numpy_ipps.utils.ndarray(
            numpy.empty(1 << order, dtype=dtype)
        )
        numpy_ipps.status = self._ipps_backend_fft(
            kernel_pad.cdata,
            self._ipps_kernel.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )

        self._ipps_spectrum = numpy_ipps.utils.ndarray(
            numpy.empty(1 << order, dtype=dtype)
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend_fft(
            src.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_mul(
            self._ipps_kernel.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spectrum.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_ifft(
            self._ipps_spectrum.cdata,
            dst.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)


@pytest.mark.parametrize("order", orders)
def test_ipps_FirFFT(benchmark, order):
    fir_fft = IPPSFirFFT(
        (1 + numpy.random.rand(1 << 4)).astype(numpy.complex64),
        8,
        dtype=numpy.complex64,
    )
    src = (1 + numpy.random.rand(1 << order)).astype(numpy.complex64)
    dst = numpy.empty(1 << order, dtype=numpy.complex64)

    with numpy_ipps.utils.context(src, dst):
        benchmark(fir_fft, src, dst)


class IPPSFirFir:
    __slots__ = (
        "_ipps_backend",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
        "_ipps_null",
    )

    def __init__(self, kernel, method, dtype=numpy.complex128):
        ipps_flag = numpy_ipps.utils.cast("int", method)
        if dtype == numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif dtype == numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        elif dtype == numpy.complex64:
            ipps_type = numpy_ipps.utils.cast("int", 14)
        elif dtype == numpy.complex128:
            ipps_type = numpy_ipps.utils.cast("int", 20)
        self._ipps_null = numpy_ipps.utils.cast("void*", 0)

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fir_getsize = numpy_ipps._detail.dispatch.ipps_function(
            "FIRSRGetSize",
            (
                "int",
                "int",
                "int*",
                "int*",
            ),
        )
        ipps_fir_init = numpy_ipps._detail.dispatch.ipps_function(
            "FIRSRInit",
            (
                "void*",
                "int",
                "int",
                "void*",
            ),
            dtype,
        )

        numpy_ipps.status = ipps_fir_getsize(
            kernel.size,
            ipps_type,
            ipps_spec_size,
            ipps_buffer_size,
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_spec_size[0], dtype=numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_buffer_size[0], dtype=numpy.uint8)
        )

        with numpy_ipps.utils.context(kernel):
            numpy_ipps.status = ipps_fir_init(
                kernel.cdata,
                kernel.size,
                ipps_flag,
                self._ipps_mem_spec.cdata,
            )

        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            "FIRSR",
            (
                "void*",
                "void*",
                "int",
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        assert src.size <= dst.size, "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            src.size,
            self._ipps_mem_spec.cdata,
            self._ipps_null,
            self._ipps_null,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("method", (0x00000001, 0x00000002))
def test_ipps_FirFir(benchmark, order, method):
    fir_fir = IPPSFirFir(
        (1 + numpy.random.rand(1 << 4)).astype(numpy.complex64),
        method=method,
        dtype=numpy.complex64,
    )
    src = (1 + numpy.random.rand(1 << order)).astype(numpy.complex64)
    dst = numpy.empty(1 << order, dtype=numpy.complex64)

    with numpy_ipps.utils.context(src, dst):
        benchmark(fir_fir, src, dst)
