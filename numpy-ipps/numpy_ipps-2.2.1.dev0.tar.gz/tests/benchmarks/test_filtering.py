import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.filtering
import numpy_ipps.filtering.fir
import numpy_ipps.policies
import numpy_ipps.support


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_filtering.log",
    )
    ch = logging.FileHandler(log_file, mode="w")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(ch)
    importlib.reload(numpy_ipps)

    yield logger

    logger.removeHandler(ch)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_FIRDirect(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.DIRECT
    )

    with numpy_ipps.utils.context(src, dst, dst_ref):
        try:
            for _retry in range(10):
                feature_obj._numpy_backend(src, dst_ref)
                feature_obj(src, dst)
                if not numpy.all(
                    numpy.abs(dst.ndarray - dst_ref.ndarray)
                    <= 6 * numpy.spacing(dst_ref.ndarray)
                ):
                    break
                src.ndarray[:] = (1 + numpy.random.rand(1 << order)).astype(
                    dtype
                )
            numpy.testing.assert_array_almost_equal_nulp(
                dst.ndarray, dst_ref.ndarray, nulp=8
            )
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_IIRDirect(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.IIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.IIR(kernel=kernel)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_IIRDirectBiQuad(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.IIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    print(kernel)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.IIR(kernel=kernel, biquad=True)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_Median(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FilterMedian.dtype_candidates:
        return

    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FilterMedian(size=12, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        try:
            for _retry in range(10):
                feature_obj._numpy_backend(src, dst_ref)
                feature_obj(src, dst)
                if not numpy.all(
                    numpy.abs(dst.ndarray - dst_ref.ndarray)
                    <= 6 * numpy.spacing(dst_ref.ndarray)
                ):
                    break
                src.ndarray[:] = (1 + numpy.random.rand(1 << order)).astype(
                    dtype
                )
            numpy.testing.assert_array_almost_equal_nulp(
                dst.ndarray, dst_ref.ndarray, nulp=8
            )
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_IIRDirect_I(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.IIR_I.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    feature_obj = numpy_ipps.filtering.IIR_I(kernel=kernel)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_IIRDirectBiQuad_I(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.IIR_I.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    print(kernel)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    feature_obj = numpy_ipps.filtering.IIR_I(kernel=kernel, biquad=True)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_Median_I(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FilterMedian_I.dtype_candidates:
        return

    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    feature_obj = numpy_ipps.filtering.FilterMedian_I(size=12, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_FIRDirectMR(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << (order - 2), dtype=dtype)
    dst_ref = numpy.empty(1 << (order - 2), dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.DIRECT, rate=(1 << 2, 1)
    )

    with numpy_ipps.utils.context(src, dst, dst_ref):
        try:
            for _retry in range(10):
                feature_obj._numpy_backend(src, dst_ref)
                feature_obj(src, dst)
                if not numpy.all(
                    numpy.abs(dst.ndarray - dst_ref.ndarray)
                    <= 6 * numpy.spacing(dst_ref.ndarray)
                ):
                    break
                src.ndarray[:] = (1 + numpy.random.rand(1 << order)).astype(
                    dtype
                )
            numpy.testing.assert_array_almost_equal_nulp(
                dst.ndarray, dst_ref.ndarray, nulp=8
            )
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_FIRDirect(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.DIRECT
    )

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_FIRDirectMR(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << (order - 2), dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.DIRECT, rate=(1 << 2, 1)
    )

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_FIRDirectFFTR(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.FFT
    )

    with numpy_ipps.utils.context(src, dst, dst_ref):
        try:
            for _retry in range(10):
                feature_obj._numpy_backend(src, dst_ref)
                feature_obj(src, dst)
                if not numpy.all(
                    numpy.abs(dst.ndarray - dst_ref.ndarray)
                    <= 6 * numpy.spacing(dst_ref.ndarray)
                ):
                    break
                src.ndarray[:] = (1 + numpy.random.rand(1 << order)).astype(
                    dtype
                )
            numpy.testing.assert_array_almost_equal_nulp(
                dst.ndarray, dst_ref.ndarray, nulp=80
            )
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_FIRDirectFFTC(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.FFT
    )

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_FIRDirectFFTR(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.FFT
    )

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_FIRDirectFFTC(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(12)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.FFT
    )

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_fir_direct(logger_fixture, benchmark, order, kernel_size, dtype):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.DIRECT
    )

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_iir_direct(logger_fixture, benchmark, order, kernel_size, dtype):
    if dtype not in numpy_ipps.filtering.IIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.IIR(kernel=kernel)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_iir_direct_biquad(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.IIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.IIR(kernel=kernel, biquad=True)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_median(logger_fixture, benchmark, order, kernel_size, dtype):
    if dtype not in numpy_ipps.filtering.FilterMedian.dtype_candidates:
        return

    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FilterMedian(size=12, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_iir_direct_I(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.IIR_I.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    feature_obj = numpy_ipps.filtering.IIR_I(kernel=kernel)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_iir_direct_biquad_I(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.IIR_I.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    feature_obj = numpy_ipps.filtering.IIR_I(kernel=kernel, biquad=True)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_median_I(logger_fixture, benchmark, order, kernel_size, dtype):
    if dtype not in numpy_ipps.filtering.FilterMedian.dtype_candidates:
        return

    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    feature_obj = numpy_ipps.filtering.FilterMedian_I(size=12, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_fir_directFFT(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.FFT
    )

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_fir_direct_cont(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.DIRECT, continuous=True
    )

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_median_cont(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.FilterMedian.dtype_candidates:
        return

    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FilterMedian(
        size=12, dtype=dtype, continuous=True
    )

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_median_cont_I(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.FilterMedian_I.dtype_candidates:
        return

    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    feature_obj = numpy_ipps.filtering.FilterMedian_I(
        size=12, dtype=dtype, continuous=True
    )

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_fir_directFFT_cont(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.FFT, continuous=True
    )

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_fir_mr_direct(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << (order - 2), dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel, method=numpy_ipps.Method.DIRECT, rate=(1 << 2, 1)
    )

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (6, 12, 18))
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_fir_mr_direct_cont(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    if dtype not in numpy_ipps.filtering.FIR.dtype_candidates:
        return

    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << (order - 2), dtype=dtype)

    feature_obj = numpy_ipps.filtering.FIR(
        kernel=kernel,
        method=numpy_ipps.Method.DIRECT,
        continuous=True,
        rate=(1 << 2, 1),
    )

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)
