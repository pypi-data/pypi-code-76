from collections.abc import Mapping


def _nested_update(repr, mapping):
    for key, val in mapping.items():
        if isinstance(val, Mapping):
            repr[key] = _nested_update(repr.get(key, {}), val)
        else:
            repr[key] = val

    return repr
