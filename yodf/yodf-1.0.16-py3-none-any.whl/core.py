from enum import Enum
import numpy as np
from .train import GradientDescentOptimizer

"""
    __init__.py of yod module does
    'from .core import *'
    Only members listed below will be accessbiel through yod when
    yod is imported as 'import yod'
    If you gets imported as 'from yod import *', then members from
    the list will go in the global import namespace which is not nice
"""
__all__ = [
    "TensorType",
    "Tensor",
    "Variable",
    "constant",
    "placeholder",
    "Session",
    "global_variables_initializer",
]


class TensorType(Enum):
    INT = 1
    FLOAT = 2


class Tensor:
    SUPPORTED_OPERATIONS = {
        # binary operations
        "add",
        "subtract",
        "divide",
        "multiply",
        "pow",
        # transcendental functions
        "sin",
        "cos",
        "reduce_mean",
        "reduce_sum",
        "log",
        "exp",
        "matmul",
        "sigmoid",
    }

    def __add__(self, other):
        from .operations import add

        return add(self, other)

    def __radd__(self, other):
        from .operations import add

        return add(other, self)

    def __sub__(self, other):
        from .operations import subtract

        return subtract(self, other)

    def __rsub__(self, other):
        from .operations import subtract

        return subtract(other, self)

    def __neg__(self):
        from .operations import multiply

        return multiply(self, -1)

    def __mul__(self, other):
        from .operations import multiply

        return multiply(self, other)

    def __rmul__(self, other):
        from .operations import multiply

        return multiply(other, self)

    def __truediv__(self, other):
        from .operations import divide

        return divide(self, other)

    def __rtruediv__(self, other):
        from .operations import divide

        return divide(other, self)

    def __pow__(self, other):
        from .operations import pow

        return pow(self, other)

    def __init__(self, dtype=None, value=None, shape=None, operation=None, inputs=None):
        if shape is not None:
            self.shape = shape
        else:
            self.shape = ()
        self.dtype = dtype
        self.value = None
        # 'if value' will not work with numpy arrays if it is not None
        if value is not None:
            self.__validate_and_set_value(value)

        if operation is not None and operation not in Tensor.SUPPORTED_OPERATIONS:
            error = f"Operation {operation} not supported. Must be one of {Tensor.SUPPORTED_OPERATIONS}."
            raise ValueError(error)
        self.operation = operation
        self.inputs = inputs

        self.gradient = None

    def __validate_and_set_value(self, value):
        if isinstance(value, int):
            self.dtype = TensorType.INT
        elif isinstance(value, float):
            self.dtype = TensorType.FLOAT
        elif isinstance(value, np.ndarray):
            if value.ndim != 2:
                raise ValueError(f"Only 2 dimensional Numpy arrays supported.")
            np_dtype = str(value.dtype)
            if np_dtype.startswith("int") or np_dtype.startswith("uint"):
                self.dtype = TensorType.INT
            elif np_dtype.startswith("float"):
                self.dtype = TensorType.FLOAT
            else:
                error = f"Numpy array with unsupported data type {np_dtype}."
                raise ValueError(error)
            self.shape = value.shape
        else:
            error = f"Unsupported Tensor Type {type(value)}."
            raise ValueError(error)
        self.value = value

    def set_gradient(self, g):
        if self.shape == ():
            self.gradient = g
        else:
            self.gradient = np.ones(self.shape) * g

    def __str__(self):
        if self.operation is None:
            return f"<yod.Tensor type={str(self.dtype)}, shape={self.shape}>"
        else:
            return f"<yod.Tensor type={str(self.dtype)}, shape={self.shape}, operation='{self.operation}'>"

    def __sigmoid(self, x):
        return 1 / (1 + np.e ** -x)

    def __reduce(self, operation):
        if operation == "sum":
            self.value = np.sum(self.inputs[0].value)
            self.gradient = np.sum(self.inputs[0].gradient)
        elif operation == "mean":
            self.value = np.mean(self.inputs[0].value)
            self.gradient = np.mean(self.inputs[0].gradient)
        else:
            error = f"Unsupported operation for reduction {operation}."
            raise ValueError(error)

    def execute(self, feed_dict=None):
        if self.operation == "add":
            self.value = self.inputs[0].value + self.inputs[1].value
            self.gradient = self.inputs[0].gradient + self.inputs[1].gradient
        elif self.operation == "subtract":
            self.value = self.inputs[0].value - self.inputs[1].value
            self.gradient = self.inputs[0].gradient - self.inputs[1].gradient
        elif self.operation == "multiply":
            self.value = self.inputs[0].value * self.inputs[1].value
            self.gradient = (
                self.inputs[0].value * self.inputs[1].gradient
                + self.inputs[0].gradient * self.inputs[1].value
            )
        elif self.operation == "divide":
            self.value = self.inputs[0].value / self.inputs[1].value
            self.gradient = (
                self.inputs[0].gradient * self.inputs[1].value
                - self.inputs[0].value * self.inputs[1].gradient
            ) / (self.inputs[1].value ** 2)
        elif self.operation == "pow":
            raise_to = self.inputs[1].value
            self.value = np.power(self.inputs[0].value, raise_to)
            self.gradient = (
                raise_to
                * np.power(self.inputs[0].value, raise_to - 1)
                * self.inputs[0].gradient
            )
        elif self.operation == "sin":
            self.value = np.sin(self.inputs[0].value)
            self.gradient = np.cos(self.inputs[0].value) * self.inputs[0].gradient
        elif self.operation == "cos":
            self.value = np.cos(self.inputs[0].value)
            self.gradient = -np.sin(self.inputs[0].value) * self.inputs[0].gradient
        elif self.operation == "log":
            self.value = np.log(self.inputs[0].value)
            self.gradient = self.inputs[0].gradient / self.inputs[0].value
        elif self.operation == "exp":
            self.value = np.e ** self.inputs[0].value
            self.gradient = self.value * self.inputs[0].gradient
        elif self.operation == "matmul":
            self.value = np.dot(self.inputs[0].value, self.inputs[1].value)
            self.gradient = np.dot(
                self.inputs[0].value, self.inputs[1].gradient
            ) + np.dot(self.inputs[0].gradient, self.inputs[1].value)
        elif self.operation == "reduce_mean":
            self.__reduce("mean")
        elif self.operation == "reduce_sum":
            self.__reduce("sum")
        elif self.operation == "sigmoid":
            self.value = self.__sigmoid(self.inputs[0].value)
            self.gradient = self.value * (1 - self.value) * self.inputs[0].gradient


class _Constant(Tensor):
    def __init__(self, value):
        super().__init__(value=value)
        self.set_gradient(0)


def constant(value):
    return _Constant(value=value)


class _PlaceHolder(Tensor):
    def __init__(self, dtype, shape=None):
        super().__init__(dtype=dtype, shape=shape)
        self.value_fed = None

    def execute(self, feed_dict=None):
        if feed_dict is None:
            raise Exception("Feed dictionary missing.")
        if feed_dict is None or self not in feed_dict:
            raise Exception("Feed dictionary missing required placeholder.")

        if self.value_fed is feed_dict[self]:
            return
        self.value_fed = feed_dict[self]

        from .operations import _convert_to_tensor

        t = _convert_to_tensor(feed_dict[self])
        self.value = t.value
        self.gradient = t.gradient


def placeholder(dtype, shape):
    return _PlaceHolder(dtype=dtype, shape=shape)


class Variable(Tensor):
    def __init__(self, initial_value):
        super().__init__(value=initial_value)
        self.set_gradient(1)
        self.__initialized = False
        _graph_completely_useless_.add_variable(self)

    def __str__(self):
        return f"<yod.Variable type={str(self.dtype)}, shape={self.shape}>"

    def initialize(self):
        self.__initialized = True

    def execute(self, feed_dict=None):
        if not self.__initialized:
            error = f"Attempt to use uninitialized variable {self}."
            raise Exception(error)


class Session:
    def __init__(self):
        global _session_yodf_
        _session_yodf_ = self
        self.tensors = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        global _session
        _session_yodf_ = None
        self.tensors = {}

    def __post_order(self, t):
        tensors_po = []

        def _append(t):
            for ti in tensors_po:
                if t is ti:
                    return
            tensors_po.append(t)

        def _traverse(t):
            if t.operation is not None:
                for ti in t.inputs:
                    _traverse(ti)
            _append(t)

        _traverse(t)
        return tensors_po

    def get_variables(self, t):
        tensors_po = self.__post_order(t)
        return list(filter(lambda t: isinstance(t, Variable), tensors_po))

    def __run(self, t, feed_dict=None):
        if isinstance(t, InitOperation):
            t.init_variables()
            return

        if isinstance(t, GradientDescentOptimizer):
            t.execute(feed_dict)
            return

        if not isinstance(t, Tensor):
            error = f"t <{t}> is not an instance of yod.Tensor."
            raise ValueError(error)

        if t not in self.tensors:
            tensors_po = self.__post_order(t)
            self.tensors[t] = tensors_po
        else:
            tensors_po = self.tensors[t]

        for tp in tensors_po:
            tp.execute(feed_dict)

        return t.value

    def run(self, t, feed_dict=None):
        if isinstance(t, list):
            values = []
            for ti in t:
                values.append(self.__run(ti, feed_dict))
            return values
        else:
            return self.__run(t, feed_dict)


# Class absolutely not needed or used for the working of the package
# Created just to be able to add something to global_variables_initializer
class Graph:
    def __init__(self):
        self.__variables = []

    def cleanup(self):
        self.__variables = []

    def add_variable(self, v):
        self.__variables.append(v)

    def get_variables(self):
        return self.__variables

    def init_variables(self):
        for v in self.__variables:
            v.initialize()


global _graph_completely_useless_
_graph_completely_useless_ = Graph()

global _session_yodf_
_session_yodf_ = None


def get_session():
    return _session_yodf_


class InitOperation:
    def __init__(self):
        self.value = None

    def init_variables(self):
        _graph_completely_useless_.init_variables()


def global_variables_initializer():
    return InitOperation()
