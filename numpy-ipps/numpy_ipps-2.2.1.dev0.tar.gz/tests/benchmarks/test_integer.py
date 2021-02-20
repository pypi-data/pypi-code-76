import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.integer
import numpy_ipps.policies
import numpy_ipps.support


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))

binary_classes = (
    numpy_ipps.AddInteger,
    numpy_ipps.MulInteger,
    numpy_ipps.SubInteger,
    numpy_ipps.DivInteger,
)
binaryI_classes = (
    numpy_ipps.AddInteger_I,
    numpy_ipps.MulInteger_I,
    numpy_ipps.SubInteger_I,
    numpy_ipps.DivInteger_I,
)

unary_classes = (
    numpy_ipps.AbsInteger,
    numpy_ipps.SqrInteger,
    numpy_ipps.SqrtInteger,
    numpy_ipps.ExpInteger,
    numpy_ipps.LnInteger,
)
unaryI_classes = (
    numpy_ipps.AbsInteger_I,
    numpy_ipps.SqrInteger_I,
    numpy_ipps.SqrtInteger_I,
    numpy_ipps.ExpInteger_I,
    numpy_ipps.LnInteger_I,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_integer.log",
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

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binary_classes)
def test_numpy_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
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

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

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
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        try:
            feature_obj._numpy_backend(src, dst_ref)
        except (NotImplementedError, TypeError):
            return

    if isinstance(feature_obj, numpy_ipps.ExpInteger):
        return
    numpy.testing.assert_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", unaryI_classes)
def test_ipps_unaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", unary_classes)
def test_numpy_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
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

    feature_obj = feature(size=1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_addproduct(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.AddProductInteger.dtype_candidates:
        return

    feature_obj = numpy_ipps.AddProductInteger(size=1 << order, dtype=dtype)
    src1 = numpy.ones(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, src_dst):
        benchmark(feature_obj, src1, src2, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_normalize(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.NormalizeInteger.dtype_candidates:
        return

    feature_obj = numpy_ipps.NormalizeInteger(size=1 << order, dtype=dtype)
    src = 3 * numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst, 1, 2)
        try:
            feature_obj._numpy_backend(src, dst_ref, 1, 2)
        except (NotImplementedError, TypeError):
            return

    numpy.testing.assert_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_normalize(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.NormalizeInteger.dtype_candidates:
        return

    feature_obj = numpy_ipps.NormalizeInteger(size=1 << order, dtype=dtype)
    src = 3 * numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst, 1, 2)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst, 1, 2)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_normalizeI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.NormalizeInteger_I.dtype_candidates:
        return

    feature_obj = numpy_ipps.NormalizeInteger_I(size=1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst, 1, 2)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_normalizeI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.NormalizeInteger_I.dtype_candidates:
        return

    feature_obj = numpy_ipps.NormalizeInteger_I(size=1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(src_dst, 1, 2)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src_dst, 1, 2)
