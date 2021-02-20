import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
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
        "test_conversion.log",
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
def test_ipps_swapbytes(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SwapBytes.dtype_candidates:
        return

    feature_obj = numpy_ipps.SwapBytes(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        try:
            feature_obj._numpy_backend(src, dst_ref)
        except (NotImplementedError, TypeError):
            return

    numpy.testing.assert_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_swapbytes(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SwapBytes.dtype_candidates:
        return

    feature_obj = numpy_ipps.SwapBytes(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_swapbytesI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SwapBytes_I.dtype_candidates:
        return

    feature_obj = numpy_ipps.SwapBytes_I(dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_swapbytesI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SwapBytes_I.dtype_candidates:
        return

    feature_obj = numpy_ipps.SwapBytes_I(dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_flip(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Flip.dtype_candidates:
        return

    feature_obj = numpy_ipps.Flip(size=1 << order, dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        try:
            feature_obj._numpy_backend(src, dst_ref)
        except (NotImplementedError, TypeError):
            return

    numpy.testing.assert_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_flip(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Flip.dtype_candidates:
        return

    feature_obj = numpy_ipps.Flip(size=1 << order, dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_flipI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Flip_I.dtype_candidates:
        return

    feature_obj = numpy_ipps.Flip_I(dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_flipI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Flip_I.dtype_candidates:
        return

    feature_obj = numpy_ipps.Flip_I(dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize(
    "src_dtype,dst_dtype",
    (
        pytest.param(
            src_dtype,
            dst_dtype,
            id="{}{}".format(numpy.dtype(src_dtype), numpy.dtype(dst_dtype)),
        )
        for src_dtype in numpy_ipps.policies.default_candidates
        for dst_dtype in numpy_ipps.policies.default_candidates
    ),
)
def test_ipps_convert(logger_fixture, benchmark, order, src_dtype, dst_dtype):
    if (src_dtype, dst_dtype) not in numpy_ipps.Convert.dtype_candidates:
        return

    feature_obj = numpy_ipps.Convert(dtype_src=src_dtype, dtype_dst=dst_dtype)
    src = numpy.empty(1 << order, dtype=src_dtype)
    dst = numpy.empty(1 << order, dtype=dst_dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize(
    "src_dtype,dst_dtype",
    (
        pytest.param(
            src_dtype,
            dst_dtype,
            id="{}{}".format(numpy.dtype(src_dtype), numpy.dtype(dst_dtype)),
        )
        for src_dtype in numpy_ipps.policies.default_candidates
        for dst_dtype in numpy_ipps.policies.default_candidates
    ),
)
def test_numpy_convert(logger_fixture, benchmark, order, src_dtype, dst_dtype):
    if (src_dtype, dst_dtype) not in numpy_ipps.Convert.dtype_candidates:
        return

    feature_obj = numpy_ipps.Convert(dtype_src=src_dtype, dtype_dst=dst_dtype)
    src = numpy.empty(1 << order, dtype=src_dtype)
    dst = numpy.empty(1 << order, dtype=dst_dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_threshold(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Threshold.dtype_candidates:
        return

    feature_obj = numpy_ipps.Threshold(dtype=dtype, level=1.5)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        try:
            feature_obj._numpy_backend(src, dst_ref)
        except (NotImplementedError, TypeError):
            return

    numpy.testing.assert_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_threshold(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Threshold.dtype_candidates:
        return

    feature_obj = numpy_ipps.Threshold(dtype=dtype, level=1.5)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_thresholdI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Threshold_I.dtype_candidates:
        return

    feature_obj = numpy_ipps.Threshold_I(dtype=dtype, level=1.5)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_thresholdI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Threshold_I.dtype_candidates:
        return

    feature_obj = numpy_ipps.Threshold_I(dtype=dtype, level=1.5)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src_dst)
