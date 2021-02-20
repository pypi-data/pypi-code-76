"""Rational Functions."""
import numpy as _numpy

import numpy_ipps._detail.metaclass.selector as _selector
import numpy_ipps.policies
import numpy_ipps.utils


class Mul:
    """Rational Mul Function."""

    __slots__ = ("_ipps_convolve",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, order, dtype, method=numpy_ipps.Method.DIRECT):
        self._ipps_convolve = numpy_ipps.Convolve(order, dtype, method=method)

    def __call__(self, src1, src2, dst):
        numerator_src1, denominator_src1 = src1.divide(2)
        numerator_src2, denominator_src2 = src2.divide(2)
        numerator_dst, denominator_dst = dst.divide(2)

        self._ipps_convolve(numerator_src1, numerator_src2, numerator_dst)
        self._ipps_convolve(
            denominator_src1, denominator_src2, denominator_dst
        )

    def _numpy_backend(self, src1, src2, dst):
        raise NotImplementedError


class MulC:
    """Rational MulC Function."""

    __slots__ = ("_ipps_mulC",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, order, dtype):
        self._ipps_mulC = numpy_ipps.MulC(order, dtype)

    def __call__(self, src, value, dst):
        numerator_src, denominator_src = src.divide(2)
        numerator_value, denominator_value = value.divide(2)
        numerator_dst, denominator_dst = dst.divide(2)

        self._ipps_mulC(
            numerator_src, numerator_value.ndarray[0], numerator_dst
        )
        self._ipps_mulC(
            denominator_src, denominator_value.ndarray[0], denominator_dst
        )

    def _numpy_backend(self, src, value, dst):
        raise NotImplementedError


class Add:
    """Rational Add Function."""

    __slots__ = (
        "_ipps_add",
        "_ipps_convolve",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.BINARY

    def __init__(self, order, dtype, method=numpy_ipps.Method.DIRECT):
        self._ipps_convolve = numpy_ipps.Convolve(order, dtype, method=method)
        self._ipps_add = numpy_ipps.Add_I(size=order, dtype=dtype)

    def __call__(self, src1, src2, dst):
        numerator_src1, denominator_src1 = src1.divide(2)
        numerator_src2, denominator_src2 = src2.divide(2)
        numerator_dst, denominator_dst = dst.divide(2)

        self._ipps_convolve(numerator_src1, denominator_src2, numerator_dst)
        self._ipps_convolve(numerator_src2, denominator_src1, denominator_dst)
        self._ipps_add(denominator_dst, numerator_dst)
        self._ipps_convolve(
            denominator_src1, denominator_src2, denominator_dst
        )

    def _numpy_backend(self, src1, src2, dst):
        raise NotImplementedError


class Eval:
    """Rational Eval Function."""

    __slots__ = (
        "_ipps_setTo",
        "_ipps_sum",
        "_ipps_mul",
        "_ipps_pow",
        "_ipps_div",
        "_ipps_power",
        "_ipps_part",
        "_ipps_value",
        "_ipps_values",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, order, dtype, accuracy=None):
        self._ipps_setTo = numpy_ipps.SetTo(size=order, dtype=dtype)
        self._ipps_sum = numpy_ipps.Sum(size=order, dtype=dtype)
        self._ipps_mul = numpy_ipps.Mul(size=order, dtype=dtype)
        self._ipps_pow = numpy_ipps.Pow(
            size=order,
            dtype=dtype,
            accuracy=accuracy
            if accuracy in numpy_ipps.Pow.ipps_accuracies
            else None,
        )
        self._ipps_div = numpy_ipps.Div(
            size=2,
            dtype=dtype,
            accuracy=accuracy
            if accuracy in numpy_ipps.Div.ipps_accuracies
            else None,
        )
        self._ipps_power = numpy_ipps.utils.ndarray(
            _numpy.arange(order, dtype=dtype)
        )
        self._ipps_part = numpy_ipps.utils.ndarray(
            _numpy.empty(order, dtype=dtype)
        )
        self._ipps_value = numpy_ipps.utils.ndarray(
            _numpy.empty(order, dtype=dtype)
        )
        self._ipps_values = numpy_ipps.utils.ndarray(
            _numpy.empty(order, dtype=dtype)
        )

    def __call__(self, src, value, dst):
        self._ipps_setTo(self._ipps_value, value)
        self._ipps_pow(self._ipps_value, self._ipps_power, self._ipps_values)

        numerator_dst, denominator_dst, eval = dst.divide(3)
        numerator_src, denominator_src = src.divide(2)

        self._ipps_mul(numerator_src, self._ipps_values, self._ipps_part)
        self._ipps_sum(self._ipps_part, numerator_dst)

        self._ipps_mul(denominator_src, self._ipps_values, self._ipps_part)
        self._ipps_sum(self._ipps_part, denominator_dst)

        self._ipps_div(numerator_dst, denominator_dst, eval)

    def _numpy_backend(self, src, value, dst):
        raise NotImplementedError


class Assign:
    """Rational Assign Function."""

    __slots__ = ("_ipps_assign",)
    dtype_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_kind = _selector.Kind.UNARY

    def __init__(self, dtype):
        self._ipps_assign = numpy_ipps.Assign(dtype=dtype)

    def __call__(self, src, dst):
        numerator_dst, denominator_dst = dst.divide(2)
        numerator_src, denominator_src = src.divide(2)

        self._ipps_assign(numerator_src, numerator_dst)
        self._ipps_assign(denominator_src, denominator_dst)

    def _numpy_backend(self, src, value, dst):
        raise NotImplementedError
