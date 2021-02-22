import numpy as np
import sys

from .core import *

__all__ = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "matmul",
    "pow",
    "square",
    "cube",
    "sin",
    "cos",
    "log",
    "exp",
    "reduce_mean",
    "reduce_sum",
    "sigmoid",
]


def _convert_to_tensor(item):
    if not isinstance(item, Tensor):
        return constant(item)
    return item


# Binary operations
def _binary_operation(a, b, op):
    a = _convert_to_tensor(a)
    b = _convert_to_tensor(b)
    return Tensor(operation=op, inputs=[a, b], dtype=a.dtype, shape=a.shape)


def add(a, b):
    op = sys._getframe().f_code.co_name
    return _binary_operation(a, b, op)


def subtract(a, b):
    op = sys._getframe().f_code.co_name
    return _binary_operation(a, b, op)


def multiply(a, b):
    op = sys._getframe().f_code.co_name
    return _binary_operation(a, b, op)


def divide(a, b):
    op = sys._getframe().f_code.co_name
    return _binary_operation(a, b, op)


def pow(a, b):
    op = sys._getframe().f_code.co_name
    return _binary_operation(a, b, op)


def square(a):
    return pow(a, 2)


def cube(a):
    return pow(a, 3)


def matmul(a, b):
    a = _convert_to_tensor(a)
    b = _convert_to_tensor(b)
    if (len(a.shape) < 2) or (len(b.shape) < 2):
        error = f"Both the arguments should be 2 dimensional arrays, dimensions passed {a.shape}, {b.shape}."
        raise ValueError(error)
    if a.shape[1] != b.shape[0]:
        error = f"Array dimensions not compatible for matrix multiplication, dimensions passed {a.shape}, {b.shape}."
        raise ValueError(error)

    op = sys._getframe().f_code.co_name
    return Tensor(
        operation=op, inputs=[a, b], dtype=a.dtype, shape=(a.shape[0], b.shape[1])
    )


# Unary operations
def _unary_operation(a, op):
    a = _convert_to_tensor(a)
    return Tensor(operation=op, inputs=[a], dtype=a.dtype, shape=a.shape)


def sin(a):
    op = sys._getframe().f_code.co_name
    return _unary_operation(a, op)


def cos(a):
    op = sys._getframe().f_code.co_name
    return _unary_operation(a, op)


def log(a):
    op = sys._getframe().f_code.co_name
    return _unary_operation(a, op)


def exp(a):
    op = sys._getframe().f_code.co_name
    return _unary_operation(a, op)


def reduce_mean(a):
    op = sys._getframe().f_code.co_name
    return _unary_operation(a, op)


def reduce_sum(a):
    op = sys._getframe().f_code.co_name
    return _unary_operation(a, op)


def sigmoid(a):
    op = sys._getframe().f_code.co_name
    return _unary_operation(a, op)
