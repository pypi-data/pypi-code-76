__all__ = ['OpenCloseMixin']

from abc import ABC
from typing import Callable, Type

from .decorators import (
    only_while_open, only_while_closed, always, check_status
)


class OpenCloseMixin(ABC):
    '''Mixin for classes with open-close dynamics.

    A boolean variable called `_open` will be set to all the instances of this
    class, in order to control whether the instance is open or not.
    It's advised not to used the `_open` variable, but the method `is_open`
    instead.

    Some methods may have a string variable called `_when`, assigned to one of
    the strings `open`, `closed` or `always`. When present, indicates when a
    method will be able to run. When not present, the value `open` is assumed.

    The user may set two variables of type :class:`~.Exception`:
        `not_open_exception`: an Exception (or subclasses) variable that will
        be raised when a method that should execute only when the instance is
        open is called when such condition is not met.

        `not_closed_exception`: an Exception (or subclasses) variable that will
        be raised when a method that should execute only when the instance is
        closed is called when such condition is not met.

    One may refer to the method name inside the exception variables messages u-
    sing the variable `method_name` enclosed in brackets.

    Example::
        class Foo(OpenCloseMixin):
            not_open_exception = RuntimeError(
                "The instance is not open, cannot call {method_name}"
            )

        # If a method called `foo` is called while the instance is closed
        # The user would see the message
        # `The instance is not open, cannot call Foo.foo`
    '''

    not_open_exception = ValueError(
        'The instance is not open and the method "{method_name}" cannot run '
        'under such condition.'
    )

    not_closed_exception = ValueError(
        'The instance is not closed and the method "{method_name}" cannot run '
        'under such condition.'
    )

    def __init_subclass__(
        cls: Type['OpenCloseMixin'], **kwargs
    ) -> Type['OpenCloseMixin']:
        setattr(cls, '__init__', always(getattr(cls, '__init__')))
        setattr(cls, 'is_open', always(getattr(cls, 'is_open')))
        setattr(cls, 'open', only_while_closed(getattr(cls, 'open')))
        setattr(cls, 'close', only_while_open(getattr(cls, 'close')))
        for attr_name in cls.__dict__:
            if isinstance(attr := getattr(cls, attr_name), Callable):
                setattr(cls, attr_name, check_status(attr))

        return cls

    def __init__(self: 'OpenCloseMixin') -> None:
        return

    def open(self: 'OpenCloseMixin') -> None:
        self._open = True

    def close(self: 'OpenCloseMixin') -> None:
        self._open = False

    def is_open(self: 'OpenCloseMixin') -> bool:
        '''Indicate if object is open.

        May be overriden in cases in which the open status depends on external
        objects.

        :return: Whether the instance is open or not
        :rtype: bool
        '''
        return getattr(self, '_open', False)
