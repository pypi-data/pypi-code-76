import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.exponential
import numpy_ipps.policies
import numpy_ipps.support


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))

unary_classes = (
    numpy_ipps.Exp,
    numpy_ipps.Exp2,
    numpy_ipps.Exp3,
    numpy_ipps.Expm1,
    numpy_ipps.Ln,
    numpy_ipps.Log2,
    numpy_ipps.Log3,
    numpy_ipps.Log10,
    numpy_ipps.Log1p,
)
unaryI_classes = (
    numpy_ipps.exponential._Exp_I,
    numpy_ipps.exponential._Expm1_I,
    numpy_ipps.Ln_I,
    numpy_ipps.exponential._Log10_I,
    numpy_ipps.Log1p_I,
)

binary_classes = (
    numpy_ipps.LogAddExp,
    numpy_ipps.LogAddExp2,
    numpy_ipps.LogAddExp3,
    numpy_ipps.xLny,
    numpy_ipps.xLog1py,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_exponential.log",
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
@pytest.mark.parametrize("feature", unary_classes)
def test_ipps_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        try:
            feature_obj._numpy_backend(src, dst_ref)
        except (NotImplementedError, TypeError):
            return

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=8)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", unaryI_classes)
def test_ipps_unaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", unary_classes)
def test_numpy_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", unaryI_classes)
def test_numpy_unaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binary_classes)
def test_ipps_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst, dst_ref):
        benchmark(feature_obj, src1, src2, dst)
        try:
            feature_obj._numpy_backend(src1, src2, dst_ref)
        except (NotImplementedError, TypeError):
            return

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=8)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binary_classes)
def test_ipps_binaryUnsafe(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst, dst_ref):
        benchmark(feature_obj, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binary_classes)
def test_numpy_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        try:
            feature_obj._numpy_backend(src1, src2, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src1, src2, dst)
