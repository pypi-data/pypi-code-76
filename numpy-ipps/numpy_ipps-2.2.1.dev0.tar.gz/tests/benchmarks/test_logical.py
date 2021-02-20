import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.logical
import numpy_ipps.policies
import numpy_ipps.support


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))

binary_classes = (
    numpy_ipps.And,
    numpy_ipps.Or,
    numpy_ipps.Xor,
)
binaryI_classes = (
    numpy_ipps.And_I,
    numpy_ipps.Or_I,
    numpy_ipps.Xor_I,
)
binaryC_classes = (
    numpy_ipps.AndC,
    numpy_ipps.OrC,
    numpy_ipps.XorC,
    numpy_ipps.LShiftC,
    numpy_ipps.RShiftC,
)
binaryCI_classes = (
    numpy_ipps.AndC_I,
    numpy_ipps.OrC_I,
    numpy_ipps.XorC_I,
    numpy_ipps.LShiftC_I,
    numpy_ipps.RShiftC_I,
)

unary_classes = (numpy_ipps.Not,)
unaryI_classes = (numpy_ipps.Not_I,)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_logical.log",
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

    feature_obj = feature(dtype=dtype)
    src1 = numpy.ones(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst, dst_ref):
        benchmark(feature_obj, src1, src2, dst)
        try:
            feature_obj._numpy_backend(src1, src2, dst_ref)
        except (NotImplementedError, TypeError):
            return

    numpy.testing.assert_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryI_classes)
def test_ipps_binaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binary_classes)
def test_numpy_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src1 = numpy.ones(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
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

    feature_obj = feature(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, src_dst):
        try:
            feature_obj._numpy_backend(src, src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryC_classes)
def test_ipps_binaryC(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    value = 1
    if dtype in (numpy.int8, numpy.uint8) and not isinstance(
        feature_obj, (numpy_ipps.LShiftC, numpy_ipps.RShiftC)
    ):
        value = numpy_ipps.utils.cast("char", value)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, value, dst)
        try:
            feature_obj._numpy_backend(src, 1, dst_ref)
        except (NotImplementedError, TypeError):
            return

    if isinstance(feature_obj, (numpy_ipps.OrC, numpy_ipps.XorC)):
        return
    numpy.testing.assert_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryCI_classes)
def test_ipps_binaryCI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    value = 1
    if dtype in (numpy.int8, numpy.uint8) and not isinstance(
        feature_obj, (numpy_ipps.logical.LShiftC_I, numpy_ipps.RShiftC_I)
    ):
        value = numpy_ipps.utils.cast("char", value)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, value, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryC_classes)
def test_numpy_binaryC(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, 1, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, 1, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryCI_classes)
def test_numpy_binaryCI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    value = 1
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(value, src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, value, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", unary_classes)
def test_ipps_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
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
@pytest.mark.parametrize("feature", unaryI_classes)
def test_ipps_unaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", unary_classes)
def test_numpy_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
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

    feature_obj = feature(dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src_dst)
