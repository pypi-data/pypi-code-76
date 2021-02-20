import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.floating
import numpy_ipps.policies
import numpy_ipps.support


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))


binary_classes = (
    numpy_ipps.Add,
    numpy_ipps.Sub,
    numpy_ipps.Mul,
    numpy_ipps.Div,
    numpy_ipps.Pow,
)
binaryI_classes = (
    numpy_ipps.Add_I,
    numpy_ipps.Sub_I,
    numpy_ipps.SubRev_I,
    numpy_ipps.Mul_I,
    numpy_ipps.Div_I,
    numpy_ipps.DivRev_I,
    numpy_ipps.floating._Pow_I,
    numpy_ipps.PowRev_I,
)

unary_classes = (
    numpy_ipps.Sqr,
    numpy_ipps.Abs,
    numpy_ipps.Sqrt,
    numpy_ipps.Cbrt,
    numpy_ipps.Inv,
    numpy_ipps.InvSqrt,
    numpy_ipps.InvCbrt,
    numpy_ipps.Pow2o3,
    numpy_ipps.Pow3o2,
)
unaryI_classes = (
    numpy_ipps.Sqr_I,
    numpy_ipps.Abs_I,
    numpy_ipps.Sqrt_I,
    numpy_ipps.Cbrt_I,
    numpy_ipps.Inv_I,
    numpy_ipps.InvSqrt_I,
    numpy_ipps.InvCbrt_I,
    numpy_ipps.Pow2o3_I,
    numpy_ipps.floating._Pow3o2_I,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_floating.log",
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

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=6)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryI_classes)
def test_ipps_binaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj, src, src_dst)


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


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryI_classes)
def test_numpy_binaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, src_dst):
        try:
            feature_obj._numpy_backend(src, src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, src_dst)


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

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=6)


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
