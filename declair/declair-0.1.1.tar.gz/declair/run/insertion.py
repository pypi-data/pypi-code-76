"""
Generic functions for insertion of special values into nested run definition
dictionaries, based on keys present in those dictonaries.
"""
from functools import wraps

def make_insert_func_recursive(insertion_key):
    # If insertion_key is not a function, assume it is an actual dictionary key
    if not callable(insertion_key):
        return make_insert_func_recursive(lambda obj: insertion_key in obj)
    def wrap(func):
        @wraps(func)
        def _recursive_insert_func(obj, *args, **kwargs):
            if isinstance(obj, list) or isinstance(obj, tuple):
                return tuple([
                    _recursive_insert_func(item, *args, **kwargs) for item in obj
                ])
            elif isinstance(obj, dict):
                if insertion_key(obj):
                    return func(obj, *args, **kwargs)
                else:
                    return {
                        key: _recursive_insert_func(value, *args, **kwargs)
                        for key, value in obj.items()
                    }
            else:
                return obj
        return _recursive_insert_func
    return wrap
