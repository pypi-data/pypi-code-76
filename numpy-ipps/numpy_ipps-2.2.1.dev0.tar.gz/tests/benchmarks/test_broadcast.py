import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.broadcast
import numpy_ipps.policies
import numpy_ipps.support


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))

binaryC_classes = (
    numpy_ipps.AddC,
    numpy_ipps.MulC,
    numpy_ipps.broadcast._SubCSelectorImpl,
    numpy_ipps.broadcast._SubCRevSelectorImpl,
    numpy_ipps.broadcast._DivCIPPSImpl,
    numpy_ipps.broadcast._DivCRevSelectorImpl,
)
binaryCI_classes = (
    numpy_ipps.AddC_I,
    numpy_ipps.MulC_I,
    numpy_ipps.broadcast._SubCSelectorImpl_I,
    numpy_ipps.broadcast._SubCRevSelectorImpl_I,
    numpy_ipps.broadcast._DivCIPPSImpl_I,
    numpy_ipps.broadcast._DivCRevSelectorImpl_I,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_broadcast.log",
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
@pytest.mark.parametrize("feature", binaryC_classes)
def test_ipps_binaryC(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)

    src = numpy.ones(1 << order, dtype=dtype)
    value = 1
    if dtype in (numpy.int8, numpy.uint8):
        value = numpy_ipps.utils.cast("char", value)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, value, dst)
        try:
            feature_obj._numpy_backend(src, 1, dst_ref)
        except (NotImplementedError, TypeError):
            return

    if dtype in numpy_ipps.policies.complex_candidates:
        return

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=6)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryCI_classes)
def test_ipps_binaryCI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    value = 1
    if dtype in (numpy.int8, numpy.uint8):
        value = numpy_ipps.utils.cast("char", value)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, value, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryC_classes)
def test_numpy_binaryC(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    value = 1
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        try:
            feature_obj._numpy_backend(src, value, dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, src, value, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
@pytest.mark.parametrize("feature", binaryCI_classes)
def test_numpy_binaryCI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature.dtype_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    value = 1
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        try:
            feature_obj._numpy_backend(value, src_dst)
        except (NotImplementedError, TypeError):
            return
        benchmark(feature_obj._numpy_backend, value, src_dst)
