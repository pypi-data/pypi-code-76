__all__ = ['always', 'only_while_closed', 'only_while_open']

from functools import wraps
from typing import Any, Callable

from .constants import ALWAYS, CLOSED, OPEN


def check_status(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(instance: Any, *args, **kwargs) -> Any:
        try:
            when = getattr(method, '_when', OPEN)

            assert(
                when == ALWAYS
                or (when == OPEN and instance.is_open())
                or (when == CLOSED and not instance.is_open())
            )
            return method(instance, *args, **kwargs)
        except AssertionError:
            exception = getattr(instance, f'not_{when.lower()}_exception')
            exception.args = (
                exception.args[0].format(method_name=method.__qualname__),
            ) + exception.args[1:]
            raise exception from None
    return wrapper


def set_required_status(status: str) -> Callable:
    '''Set the required status an instance must have in order for a method to
    be able to run.

    :param status: one of the following strings: `open`, `closed` or `always`
    :type status: str
    :return: the same decorator with a specific status as argument
    :rtype: Callable[[Callable], Callable]
    '''
    def decorator(method: Callable) -> Callable:
        '''Mark a method to be able to run {condition}.

        A variable named `_when` is set for the purpose of this function.

        :param method: the method to be marked
        :type method: Callable
        :return: the same method, now marked
        :rtype: Callable
        '''
        setattr(method, '_when', status)
        return method
    return decorator


only_while_closed = set_required_status(CLOSED)
only_while_closed.__doc__ = only_while_closed.__doc__.format(
    condition='only while the instance is open'
)

only_while_open = set_required_status(OPEN)
only_while_open.__doc__ = only_while_open.__doc__.format(
    condition='only while the instance is closed'
)

always = set_required_status(ALWAYS)
always.__doc__ = always.__doc__.format(
    condition='always'
)
