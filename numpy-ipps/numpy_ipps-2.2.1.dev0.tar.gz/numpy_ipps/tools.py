"""Miscelenous tools."""
import numpy as _numpy

import numpy_ipps.policies
import numpy_ipps.rational
import numpy_ipps.utils


@numpy_ipps.utils.disable_gc
def sumN(*args):
    """Sum of N rationals."""
    lhs, rhs, *others = args

    add = numpy_ipps.rational.Add(
        order=((int(lhs.size) - 2) << (len(others) + 1)) + 2,
        dtype=lhs.ndarray.dtype,
    )
    result = numpy_ipps.utils.ndarray(
        _numpy.empty((int(lhs.size) - 1) << 1, dtype=lhs.ndarray.dtype)
    )
    add(lhs, rhs, result)

    assign = numpy_ipps.rational.Assign(dtype=lhs.ndarray.dtype)
    for a in others:
        lhs = result
        rhs = numpy_ipps.utils.ndarray(
            _numpy.zeros(int(lhs.size), dtype=lhs.ndarray.dtype)
        )
        assign(a, rhs)
        result = numpy_ipps.utils.ndarray(
            _numpy.empty((int(lhs.size) - 1) << 1, dtype=lhs.ndarray.dtype)
        )
        add(lhs, rhs, result)
    return result


@numpy_ipps.utils.disable_gc
def bbp(a, base, dtype):
    """Bailey–Borwein–Plouffe formula."""
    if dtype is _numpy.float32:
        digitN = int(_numpy.fix(24 / _numpy.log2(base)))

    elif dtype is _numpy.float64:
        digitN = int(_numpy.fix(53 / _numpy.log2(base)))
    else:
        raise RuntimeError("Invalid dtype.")

    digit = numpy_ipps.utils.ndarray(_numpy.arange(digitN, dtype=dtype))

    eval = numpy_ipps.rational.Eval(
        int(a.size) >> 1,
        dtype=a.ndarray.dtype,
        accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
    )

    frac = numpy_ipps.utils.ndarray(
        _numpy.empty(3 * digitN, dtype=a.ndarray.dtype)
    )

    for value, dst in zip(digit.ndarray, frac.divide(digitN)):
        eval(a, value, dst)

    frac.ndarray[2::3] = _numpy.fmod(frac.ndarray[2::3], base)
    frac.ndarray[0::3] = base * _numpy.fmod(
        frac.ndarray[0::3], frac.ndarray[1::3]
    )

    remainder = _numpy.zeros(digitN, dtype=a.ndarray.dtype)
    epsilon = _numpy.zeros(digitN, dtype=a.ndarray.dtype)
    result = numpy_ipps.utils.ndarray(_numpy.zeros(digitN, dtype=dtype))

    result.ndarray[0] = _numpy.fix(frac.ndarray[2])
    remainder[0] = frac.ndarray[0]
    epsilon[0] = 0

    for i in range(1, digitN):
        remainder[i] = (
            (base * frac.ndarray[1 + 3 * i])
            * _numpy.fmod(remainder[i - 1], frac.ndarray[-2 + 3 * i])
        ) / frac.ndarray[-2 + 3 * i]
        epsilon[i] = _numpy.maximum(
            2 * _numpy.spacing(remainder[i]),
            ((base * frac.ndarray[1 + 3 * i]) * epsilon[i - 1])
            / frac.ndarray[-2 + 3 * i],
        )
        remainder[i] = frac.ndarray[3 * i] + remainder[i]

        if remainder[i] < 2 * base * epsilon[i]:
            i -= 1
            break

        result.ndarray[i] = _numpy.fix(
            _numpy.fmod(
                _numpy.fmod(remainder[i - 1] / frac.ndarray[-2 + 3 * i], base)
                + frac.ndarray[2 + 3 * i],
                base,
            )
        )

    value = numpy_ipps.utils.ndarray(base * _numpy.ones(i + 1, dtype=dtype))
    values = numpy_ipps.utils.ndarray(_numpy.empty(i + 1, dtype=dtype))
    terms = numpy_ipps.utils.ndarray(_numpy.empty(i + 1, dtype=dtype))
    dst = numpy_ipps.utils.ndarray(_numpy.empty(1, dtype=dtype))

    sum = numpy_ipps.Sum(size=i + 1, dtype=dtype)
    div = numpy_ipps.Div(
        size=i + 1,
        dtype=dtype,
        accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
    )
    pow = numpy_ipps.Pow(
        size=i + 1,
        dtype=dtype,
        accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
    )

    pow(value, digit.slice(stop=i + 1), values)
    div(result.slice(stop=i + 1), values, terms)
    sum(terms, dst)

    return dst


@numpy_ipps.utils.disable_gc
def series(gen, dtype):
    """Sum of a series."""
    if dtype is _numpy.float32:
        digitN = 24
    elif dtype is _numpy.float64:
        digitN = 53
    else:
        raise RuntimeError("Invalid dtype.")

    assign = numpy_ipps.Assign(dtype=dtype)
    result = numpy_ipps.utils.ndarray(_numpy.zeros(digitN, dtype=dtype))

    for i, (digit, value) in enumerate(zip(result.divide(digitN), gen)):
        if i == 0:
            assign(value, digit)
            epsilon = _numpy.spacing(value.ndarray[0])
            continue

        if -epsilon / 2 < dtype(value[0]) < epsilon / 2:
            i -= 1
            break

        assign(value, digit)

    dst = numpy_ipps.utils.ndarray(_numpy.empty(1, dtype=dtype))

    sum = numpy_ipps.Sum(size=i + 1, dtype=dtype)
    sum(result.slice(stop=i + 1), dst)

    return dst
