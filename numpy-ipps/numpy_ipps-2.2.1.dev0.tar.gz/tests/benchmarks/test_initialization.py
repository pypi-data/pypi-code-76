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
        "test_initialization.log",
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
def test_ipps_assign(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Assign.dtype_candidates:
        return

    assign = numpy_ipps.Assign(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign, src, dst)

    numpy.testing.assert_equal(dst, src)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_assign(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Assign.dtype_candidates:
        return

    assign = numpy_ipps.Assign(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign._numpy_backend, src, dst)

    numpy.testing.assert_equal(dst, src)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_bitshiftLE(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.BitShift.dtype_candidates:
        return

    bitshift_le = numpy_ipps.BitShift(3, 5, numpy_ipps.Endian.LITTLE)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    size = 8 * (1 << order) - 12

    with numpy_ipps.utils.context(src, dst):
        benchmark(bitshift_le, src, dst, size)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_bitshiftBE(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.BitShift.dtype_candidates:
        return

    bitshift_be = numpy_ipps.BitShift(3, 5, numpy_ipps.Endian.BIG)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    size = 8 * (1 << order) - 12

    with numpy_ipps.utils.context(src, dst):
        benchmark(bitshift_be, src, dst, size)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_set0(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Zeros.dtype_candidates:
        return

    zeros = numpy_ipps.Zeros(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src):
        benchmark(zeros, src)

    numpy.testing.assert_equal(src, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_ipps_set1(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SetTo.dtype_candidates:
        return

    set_to_1 = numpy_ipps.SetTo(size=1 << order, dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    value = 2
    if dtype in (numpy.int8, numpy.uint8):
        value = numpy_ipps.utils.cast("char", value)

    with numpy_ipps.utils.context(src):
        benchmark(set_to_1, src, value)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_set0(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Zeros.dtype_candidates:
        return

    zeros = numpy_ipps.Zeros(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src):
        benchmark(zeros._numpy_backend, src)

    numpy.testing.assert_equal(src, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", numpy_ipps.policies.default_candidates)
def test_numpy_set1(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SetTo.dtype_candidates:
        return

    set_to_1 = numpy_ipps.SetTo(size=1 << order, dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    value = 2

    with numpy_ipps.utils.context(src):
        benchmark(set_to_1._numpy_backend, src, value)
