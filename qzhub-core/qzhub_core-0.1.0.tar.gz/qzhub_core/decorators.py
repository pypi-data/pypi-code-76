import functools
import logging
from constants import DEPRECATION_MESSAGE

logger = logging.getLogger(__name__)


def deprecate(recommended_function):
    def decorator_deprecate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            deprecated_function = func.__name__
            logger.warning(
                DEPRECATION_MESSAGE % (deprecated_function, recommended_function)
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator_deprecate