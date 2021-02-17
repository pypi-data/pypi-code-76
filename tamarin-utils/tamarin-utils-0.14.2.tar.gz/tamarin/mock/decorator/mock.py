from functools import wraps
from typing import Dict


def mock(func_list: dict, condition: str):
    """
    :return: return response and say that request has error or not
    """

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if condition:
                if condition.lower() == 'test':
                    return func_list.get('test', func)(*args, **kwargs)
                elif condition.lower() == 'development':  # pragma: no cover
                    return func_list.get('development', func)(*args, **kwargs)
                elif condition.lower() == 'staging':  # pragma: no cover
                    return func_list.get('staging', func)(*args, **kwargs)
                elif condition.lower() == 'production':  # pragma: no cover
                    return func_list.get('production', func)(*args, **kwargs)
            return func(*args, **kwargs)

        return inner

    return decorator
