import random


def set_seed(seed):
    def wrapper(fn):
        def inner(*args, **kwargs):
            random.seed(seed)
            return fn(*args, **kwargs)
        return inner
    return wrapper
