import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.policies
import numpy_ipps.rational
import numpy_ipps.support


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))

binary_classes = (
    numpy_ipps.rational.Add,
    numpy_ipps.rational.Mul,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_signal.log",
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

    feature_obj = feature(order=1 << (order - 1), dtype=dtype)
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty((1 << (order + 1)) - 2, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(feature_obj, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binary_classes)
def test_numpy_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(order=1 << (order - 1), dtype=dtype)
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty((1 << (order + 1)) - 2, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        try:
            feature_obj._numpy_backend(src1, src2, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_eval(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.rational.Eval.dtype_candidates:
        return

    feature_obj = numpy_ipps.rational.Eval(order=1 << (order - 1), dtype=dtype)

    src = numpy.ones(1 << order, dtype=dtype)
    value = 2
    if dtype in (numpy.int8, numpy.uint8):
        value = numpy_ipps.utils.cast("char", value)
    dst = numpy.empty(3, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, value, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_assign(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.rational.Assign.dtype_candidates:
        return

    feature_obj = numpy_ipps.rational.Assign(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << (order + 1), dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)
