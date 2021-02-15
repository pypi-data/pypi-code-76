import numpy as np

int_types = [int, np.int8, np.int16, np.int32, np.int64]
float_types = [float, np.float16, np.float32, np.float64]

number_types = []
number_types.extend(int_types)
number_types.extend(float_types)

iterable_jsonable_types = [
    dict, list, tuple, str
]
noniterable_jsonable_types = [
    int, float, bool,
    type(None)
]
jsonable_types = iterable_jsonable_types + noniterable_jsonable_types