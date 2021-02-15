"""This module implements the ``Nothing`` part of the ``Maybe`` monad.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

from typing_extensions import Literal

if t.TYPE_CHECKING:  # pragma: no cover
    # pylint: disable=unused-import,invalid-name
    from ._maybe import Maybe

_T = t.TypeVar('_T', covariant=True)
_TT = t.TypeVar('_TT', covariant=True)
_Y = t.TypeVar('_Y')


class _Nothing(t.Generic[_T]):
    """Singleton class to represent the ``Nothing`` part of a ``Maybe``.
    """
    __slots__ = ()

    is_just: Literal[False] = False
    is_nothing: Literal[True] = True

    # pylint: disable=no-self-use,missing-function-docstring
    def map(self, _mapper: t.Callable[[_T], _TT]) -> '_Nothing[_TT]':
        return Nothing

    def map_or_default(
        self,
        mapper: t.Callable[[_T], _Y],  # pylint: disable=unused-argument
        default: _Y,
    ) -> _Y:
        return default

    def chain(
        self, _chainer: t.Callable[[_T], 'Maybe[_TT]']
    ) -> '_Nothing[_TT]':
        return Nothing

    def alt(self, alternative: 'Maybe[_T]') -> 'Maybe[_T]':
        return alternative

    def alt_lazy(
        self, maker: t.Callable[[], 'Maybe[_Y]']
    ) -> 'Maybe[t.Union[_Y, _T]]':
        return maker()

    def or_default(self, value: _Y) -> _Y:
        return value

    def or_default_lazy(self, _producer: t.Callable[[], _Y]) -> _Y:
        return _producer()

    def unsafe_extract(self) -> _T:
        raise AssertionError('Tried to extract a _Nothing')

    def case_of(
        self,
        *,
        just: t.Callable[[_T], _TT],  # pylint: disable=unused-argument
        nothing: t.Callable[[], _TT],
    ) -> _TT:
        return nothing()

    def if_just(self, callback: t.Callable[[_T], object]) -> '_Nothing[_T]':  # pylint: disable=unused-argument
        return self

    def if_nothing(self, callback: t.Callable[[], object]) -> '_Nothing[_T]':
        callback()
        return self

    def try_extract(
        self, make_exception: t.Union[t.Callable[[], Exception], Exception]
    ) -> t.NoReturn:
        if isinstance(make_exception, Exception):
            raise make_exception
        raise make_exception()

    def __repr__(self) -> str:
        return 'Nothing'

    @classmethod
    def is_nothing_instance(cls, obj: object) -> bool:
        """Check if the given object is a Nothing object.

        >>> from ._just import Just
        >>> Nothing.is_nothing_instance(5)
        False
        >>> Nothing.is_nothing_instance(Nothing)
        True
        >>> Nothing.is_nothing_instance(Just(5))
        False
        """
        return isinstance(obj, cls)

    def __bool__(self) -> t.NoReturn:
        raise Exception('Do not check Nothing for boolean value')

    # pylint: enable=no-self-use,missing-function-docstring


Nothing: _Nothing[t.Any] = _Nothing()
