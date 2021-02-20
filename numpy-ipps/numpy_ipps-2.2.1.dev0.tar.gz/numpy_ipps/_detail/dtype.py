import ctypes

import numpy

import numpy_ipps._detail.debug


def as_ctypes_type(dtype):
    try:
        return numpy.ctypeslib.as_ctypes(numpy.empty(0, dtype=dtype))._type_
    except KeyError:
        raise NotImplementedError


def to_float(dtype):
    ctype_type = as_ctypes_type(dtype)
    if ctype_type in (
        as_ctypes_type(numpy.dtype(ctypes.c_uint8)),
        as_ctypes_type(numpy.dtype(ctypes.c_int8)),
    ):
        return ctypes.c_float
    elif ctype_type in (
        as_ctypes_type(numpy.dtype(ctypes.c_uint16)),
        as_ctypes_type(numpy.dtype(ctypes.c_int16)),
    ):
        return ctypes.c_float
    elif ctype_type in (
        as_ctypes_type(numpy.dtype(ctypes.c_uint32)),
        as_ctypes_type(numpy.dtype(ctypes.c_int32)),
    ):
        return ctypes.c_float
    elif ctype_type == as_ctypes_type(numpy.dtype(ctypes.c_float)):
        return ctypes.c_float
    elif ctype_type in (
        as_ctypes_type(numpy.dtype(ctypes.c_uint64)),
        as_ctypes_type(numpy.dtype(ctypes.c_int64)),
    ):
        return ctypes.c_double
    elif ctype_type == as_ctypes_type(numpy.dtype(ctypes.c_double)):
        return ctypes.c_double
    else:
        numpy_ipps._detail.debug.log_and_raise(
            RuntimeError, "Unknown dtype: {}".format(dtype), name=__name__
        )


def remove_complex(dtype):
    if dtype == numpy.complex64:
        return ctypes.c_float
    elif dtype == numpy.complex128:
        return ctypes.c_double
    return as_ctypes_type(dtype)
