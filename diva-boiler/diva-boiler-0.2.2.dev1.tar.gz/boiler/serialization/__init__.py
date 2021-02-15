from functools import wraps
from typing import Callable, Iterable

from boiler.models import ActivityList


SerializeToFile = Callable[[str, Iterable[ActivityList]], None]


class ParseError(Exception):
    pass


def error_handler(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ParseError:
                raise
            except Exception as e:
                raise ParseError(message) from e

        return wrapper

    return decorator
