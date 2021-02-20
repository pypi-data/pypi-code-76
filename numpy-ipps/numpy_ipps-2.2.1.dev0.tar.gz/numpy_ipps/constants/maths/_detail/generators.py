import numpy

import numpy_ipps.utils


class e:
    __slots__ = (
        "_ipps_one",
        "_ipps_index",
        "_ipps_current",
        "_ipps_add",
        "_ipps_div",
        "_first",
    )

    def __init__(self, dtype):
        self._ipps_one = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_index = numpy_ipps.utils.ndarray(
            numpy.array([0], dtype=dtype)
        )
        self._ipps_current = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )

        self._ipps_add = numpy_ipps.Add_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_div = numpy_ipps.DivRev_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._first = True

    def __iter__(self):
        return self

    def __next__(self):
        if self._first:
            self._first = False
            return self._ipps_current
        self._ipps_add(self._ipps_one, self._ipps_index)
        self._ipps_div(self._ipps_index, self._ipps_current)
        return self._ipps_current


class I1:
    __slots__ = (
        "_ipps_one",
        "_ipps_lhs",
        "_ipps_rhs",
        "_ipps_index",
        "_ipps_current",
        "_ipps_add",
        "_ipps_mul",
        "_ipps_pow",
        "_ipps_inv",
    )

    def __init__(self, dtype):
        self._ipps_one = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_lhs = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_rhs = numpy_ipps.utils.ndarray(
            numpy.array([-1], dtype=dtype)
        )
        self._ipps_index = numpy_ipps.utils.ndarray(
            numpy.array([0], dtype=dtype)
        )
        self._ipps_current = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )

        self._ipps_add = numpy_ipps.Add_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_mul = numpy_ipps.Mul_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_pow = numpy_ipps.Pow(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_inv = numpy_ipps.Inv_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )

    def __iter__(self):
        return self

    def __next__(self):
        self._ipps_add(self._ipps_one, self._ipps_index)
        self._ipps_pow(self._ipps_index, self._ipps_index, self._ipps_current)
        self._ipps_inv(self._ipps_current)
        self._ipps_mul(self._ipps_lhs, self._ipps_current)
        numpy_ipps.utils.swap_ndarray(self._ipps_lhs, self._ipps_rhs)
        return self._ipps_current


class I2:
    __slots__ = (
        "_ipps_one",
        "_ipps_index",
        "_ipps_current",
        "_ipps_add",
        "_ipps_pow",
        "_ipps_inv",
    )

    def __init__(self, dtype):
        self._ipps_one = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_index = numpy_ipps.utils.ndarray(
            numpy.array([0], dtype=dtype)
        )
        self._ipps_current = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )

        self._ipps_add = numpy_ipps.Add_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_pow = numpy_ipps.Pow(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_inv = numpy_ipps.Inv_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )

    def __iter__(self):
        return self

    def __next__(self):
        self._ipps_add(self._ipps_one, self._ipps_index)
        self._ipps_pow(self._ipps_index, self._ipps_index, self._ipps_current)
        self._ipps_inv(self._ipps_current)
        return self._ipps_current


class EB:
    __slots__ = (
        "_ipps_one",
        "_ipps_two",
        "_ipps_current",
        "_ipps_currentInv",
        "_ipps_add",
        "_ipps_mul",
        "_ipps_inv",
    )

    def __init__(self, dtype):
        self._ipps_one = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_two = numpy_ipps.utils.ndarray(
            numpy.array([2], dtype=dtype)
        )
        self._ipps_currentInv = numpy_ipps.utils.ndarray(
            numpy.array([0], dtype=dtype)
        )
        self._ipps_current = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )

        self._ipps_add = numpy_ipps.Add_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_mul = numpy_ipps.Mul_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_inv = numpy_ipps.Inv(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )

    def __iter__(self):
        return self

    def __next__(self):
        self._ipps_mul(self._ipps_two, self._ipps_currentInv)
        self._ipps_add(self._ipps_one, self._ipps_currentInv)
        self._ipps_inv(self._ipps_currentInv, self._ipps_current)
        return self._ipps_current


class G:
    __slots__ = (
        "_ipps_two",
        "_ipps_lhs",
        "_ipps_rhs",
        "_ipps_index",
        "_ipps_current",
        "_ipps_add",
        "_ipps_div",
        "_ipps_sqr",
    )

    def __init__(self, dtype):
        self._ipps_two = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_lhs = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_rhs = numpy_ipps.utils.ndarray(
            numpy.array([-1], dtype=dtype)
        )
        self._ipps_index = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_current = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )

        self._ipps_add = numpy_ipps.Add_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_div = numpy_ipps.Div_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_sqr = numpy_ipps.Sqr(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )

    def __iter__(self):
        return self

    def __next__(self):
        self._ipps_sqr(self._ipps_index, self._ipps_current)
        self._ipps_div(self._ipps_lhs, self._ipps_current)
        numpy_ipps.utils.swap_ndarray(self._ipps_lhs, self._ipps_rhs)
        self._ipps_add(self._ipps_two, self._ipps_index)
        return self._ipps_current


class zeta3:
    __slots__ = (
        "_ipps_one",
        "_ipps_three",
        "_ipps_index",
        "_ipps_current",
        "_ipps_add",
        "_ipps_pow",
        "_ipps_inv",
    )

    def __init__(self, dtype):
        self._ipps_one = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_three = numpy_ipps.utils.ndarray(
            numpy.array([3], dtype=dtype)
        )
        self._ipps_index = numpy_ipps.utils.ndarray(
            numpy.array([0], dtype=dtype)
        )
        self._ipps_current = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )

        self._ipps_add = numpy_ipps.Add_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_pow = numpy_ipps.Pow(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_inv = numpy_ipps.Inv_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )

    def __iter__(self):
        return self

    def __next__(self):
        self._ipps_add(self._ipps_one, self._ipps_index)
        self._ipps_pow(self._ipps_index, self._ipps_three, self._ipps_current)
        self._ipps_inv(self._ipps_current)
        return self._ipps_current


class ePi:
    __slots__ = (
        "_ipps_one",
        "_ipps_index",
        "_ipps_current",
        "_ipps_add",
        "_ipps_mul",
        "_ipps_div",
        "_first",
        "_pi",
    )

    def __init__(self, pi, dtype):
        self._pi = pi

        self._ipps_one = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )
        self._ipps_index = numpy_ipps.utils.ndarray(
            numpy.array([0], dtype=dtype)
        )
        self._ipps_current = numpy_ipps.utils.ndarray(
            numpy.array([1], dtype=dtype)
        )

        self._ipps_add = numpy_ipps.Add_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_mul = numpy_ipps.Mul_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._ipps_div = numpy_ipps.DivRev_I(
            size=1,
            dtype=dtype,
            accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
        )
        self._first = True

    def __iter__(self):
        return self

    def __next__(self):
        if self._first:
            self._first = False
            return self._ipps_current
        self._ipps_add(self._ipps_one, self._ipps_index)
        self._ipps_mul(self._pi, self._ipps_current)
        self._ipps_div(self._ipps_index, self._ipps_current)
        return self._ipps_current
