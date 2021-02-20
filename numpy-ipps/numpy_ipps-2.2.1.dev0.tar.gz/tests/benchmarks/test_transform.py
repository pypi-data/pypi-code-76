import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.transform


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))

unary_classes = (
    numpy_ipps.transform.FFTFwd,
    numpy_ipps.transform.FFTInv,
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
@pytest.mark.parametrize("feature", unary_classes)
def test_ipps_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(order=order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", unary_classes)
def test_numpy_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(order=order, dtype=dtype)
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
def test_ipps_hilbert(logger_fixture, benchmark, order, dtype):
    feature = numpy_ipps.transform.Hilbert
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(order=order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype().real.dtype.type)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_hilbert(logger_fixture, benchmark, order, dtype):
    feature = numpy_ipps.transform.Hilbert
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(order=order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype().real.dtype.type)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, dst)
