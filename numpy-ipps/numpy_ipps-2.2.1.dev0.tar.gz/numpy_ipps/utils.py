"""Utility classes and functions."""
import ctypes as _ctypes
import functools as _functools
import gc as _gc
import inspect as _inspect

import numpy as _numpy
import regex as _regex

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.libipp as _libipp


cast = _libipp.ffi.cast
new = _libipp.ffi.new


class ndarray:
    """Wrapper class for numpy.ndarray for cffi."""

    __slots__ = ("ndarray", "cdata", "size", "shape")

    def __init__(self, array=None):
        if __debug__ and array is not None and not array.flags["C_CONTIGUOUS"]:
            _debug.log_and_raise(
                AssertionError, "Array is not C_CONTIGUOUS.", name=__name__
            )

        self.ndarray = array
        self.cdata = cast(
            "void*",
            0 if array is None else _libipp.ffi.from_buffer(array),
        )
        self.size = cast("int", 0 if array is None else array.size)
        self.shape = new("int[]", (0,) if array is None else array.shape)

    def __repr__(self):
        return "<numpy_ipps.ndarray '{}' 0x{:016x} size {}>".format(
            self.ndarray.dtype,
            int(cast("unsigned int", self.cdata)),
            int(self.size),
        )

    def divide(self, n):
        """Divide a ndarray to n ndarray."""
        size = int(self.size) // n
        flatten = _numpy.ravel(self.ndarray)

        for i in range(n - 1):
            yield ndarray(flatten[i * size : (i + 1) * size])

        yield ndarray(flatten[(n - 1) * size :])

    def slice(self, start=None, stop=None, k=None):
        """Take a slice of a ndarray."""
        return ndarray(_numpy.ravel(self.ndarray)[start:stop])

    def __getitem__(self, index):
        return cast(
            _dispatch.as_ctype_str(self.ndarray.dtype), self.ndarray[index]
        )


def swap_ndarray(ndarray_lhs, ndarray_rhs):
    """Swap two ndarray wrapper."""
    if __debug__ and int(ndarray_lhs.size) != int(ndarray_rhs.size):
        _debug.log_and_raise(
            AssertionError,
            "Incompatible size arrays {} != {}.".format(
                int(ndarray_lhs.size), int(ndarray_rhs.size)
            ),
            name=__name__,
        )

    ndarray_tmp = ndarray_lhs.ndarray
    cdata_tmp = ndarray_lhs.cdata

    ndarray_lhs.ndarray = ndarray_rhs.ndarray
    ndarray_lhs.cdata = ndarray_rhs.cdata

    ndarray_rhs.ndarray = ndarray_tmp
    ndarray_rhs.cdata = cdata_tmp


class context:
    """Context manager for user-friendly access."""

    __slots__ = (
        "symbols",
        "_gc_reenable",
        "_outer_frame",
        "_outer_frame_ptr",
        "_PyFrame_flag",
    )
    _pattern = _regex.compile(
        r".*context\s*\(((?:[^,()]+)(?:,[^,()]+)*)\).*", _regex.V1
    )

    def __init__(self, *args):
        self._outer_frame = _inspect.currentframe().f_back
        self._outer_frame_ptr = _ctypes.py_object(self._outer_frame)
        self._PyFrame_flag = _ctypes.c_int(0)
        self.symbols = (
            _regex.search(
                context._pattern,
                _inspect.getframeinfo(self._outer_frame).code_context[0],
            )
            .group(1)
            .replace(" ", "")
            .split(",")
        )
        self._gc_reenable = _gc.isenabled()

    def _LocalsToFast(self):
        _ctypes.pythonapi.PyFrame_LocalsToFast(
            self._outer_frame_ptr, self._PyFrame_flag
        )

    def __enter__(self):
        if self._gc_reenable:
            _gc.disable()

        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = ndarray(
                self._outer_frame.f_locals[symbol]
            )
            self._LocalsToFast()

    def __exit__(self, *args):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = self._outer_frame.f_locals[
                symbol
            ].ndarray
            self._LocalsToFast()

        if self._gc_reenable:
            _gc.enable()

        return False


def disable_gc(fun):
    """Decorate a function to disable garbage collector."""

    @_functools.wraps(fun)
    def wrapper(*args, **kwargs):
        gc_reenable = _gc.isenabled()

        if gc_reenable:
            _gc.disable()

        result = fun(*args, **kwargs)

        if gc_reenable:
            _gc.enable()

        return result

    return wrapper
