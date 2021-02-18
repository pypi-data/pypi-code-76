from xbokeh.common.assertions import assert_types
import numpy as np


def validate_data(data: dict):
    keys = list(data.keys())
    assert len(keys) == len(set(keys)), f"Duplicated key exists in data: {keys}"
    assert all(k in data for k in ["x", "y"]), f"x and y are required field of data: {data.keys()}"

    size = None
    for k in data:
        d = data[k]
        assert_types(d, "data", [list, np.ndarray])
        if size is None:
            size = len(d)
        else:
            assert len(d) == size, f"data value size unmatched: {len(d)}, {size}"
