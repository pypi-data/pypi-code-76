import enum

import numpy

import numpy_ipps.support


class Kind(enum.Enum):
    UNARY_I = 1
    UNARY = 2
    BINARY_I = 2
    BINARY = 3


class Selector(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_class,
        numpy_class,
        numpy_types_L1=tuple(),
        numpy_types_L2=tuple(),
    ):
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_class = ipps_class
        cls._numpy_class = numpy_class
        cls._dtype_candidates_L1 = numpy_types_L1
        cls._dtype_candidates_L2 = numpy_types_L2

        cls.dtype_candidates = ipps_class.dtype_candidates

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, size, dtype):
        if numpy_ipps.disable_numpy:
            return cls._ipps_class(dtype=dtype, size=size)

        if dtype in cls._dtype_candidates_L1:
            self = cls._numpy_class(dtype=dtype, size=size)
        elif (
            dtype not in cls._dtype_candidates_L2
            or cls._ipps_class._ipps_kind.value * numpy.dtype(dtype).itemsize
            < numpy_ipps.support.L1
        ):
            self = cls._ipps_class(dtype=dtype, size=size)
        else:
            self = cls._numpy_class(dtype=dtype, size=size)

        return self


class SelectorAccuracy(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_class,
        numpy_class,
        numpy_types_L1=tuple(),
        numpy_types_L2=tuple(),
    ):
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_class = ipps_class
        cls._numpy_class = numpy_class
        cls._dtype_candidates_L1 = numpy_types_L1
        cls._dtype_candidates_L2 = numpy_types_L2

        cls.dtype_candidates = ipps_class.dtype_candidates
        cls.ipps_accuracies = ipps_class.ipps_accuracies

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, size, dtype, accuracy=None):
        if numpy_ipps.disable_numpy or accuracy is not None:
            return cls._ipps_class(dtype=dtype, size=size, accuracy=accuracy)

        if dtype in cls._dtype_candidates_L1:
            self = cls._numpy_class(dtype=dtype, size=size, accuracy=accuracy)
        elif (
            dtype not in cls._dtype_candidates_L2
            or cls._ipps_class._ipps_kind.value * numpy.dtype(dtype).itemsize
            < numpy_ipps.support.L1
        ):
            self = cls._ipps_class(dtype=dtype, size=size, accuracy=accuracy)
        else:
            self = cls._numpy_class(dtype=dtype, size=size, accuracy=accuracy)

        return self
