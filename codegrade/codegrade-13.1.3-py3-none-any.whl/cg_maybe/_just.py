"""This module implements the ``Just`` part of the ``Maybe`` monad.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

from typing_extensions import Final, Literal

if t.TYPE_CHECKING:  # pragma: no cover
    # pylint: disable=unused-import,invalid-name
    from ._maybe import Maybe

_T = t.TypeVar('_T', covariant=True)
_TT = t.TypeVar('_TT', covariant=True)
_Y = t.TypeVar('_Y')


class Just(t.Generic[_T]):
    """The just part of the Maybe monad.
    """
    __slots__ = ('value', )

    is_just: Literal[True] = True
    is_nothing: Literal[False] = False

    def __init__(self, value: _T) -> None:
        self.value: Final = value

    def map(self, mapper: t.Callable[[_T], _TT]) -> 'Just[_TT]':
        """Transform this just by applying ``mapper`` to its argument and
        wrapping the result in a new ``Just``.

        >>> from ._nothing import Nothing
        >>> Just(5).map(lambda el: el * el)
        Just(25)
        >>> Nothing.map(lambda el: el * el)
        Nothing
        """
        return Just(mapper(self.value))

    def map_or_default(
        self,
        mapper: t.Callable[[_T], _Y],
        default: _Y,  # pylint: disable=unused-argument
    ) -> _Y:
        """Transform this just by applying ``mapper`` to its argument and
        return the result.

        >>> from ._nothing import Nothing
        >>> Just(5).map_or_default(lambda el: el * el, 10)
        25
        >>> Nothing.map_or_default(lambda el: el * el, 10)
        10
        """
        return mapper(self.value)

    def chain(self, chainer: t.Callable[[_T], 'Maybe[_TT]']) -> 'Maybe[_TT]':
        """Transforms ``this`` with a function that returns a ``Maybe``.

        >>> from ._nothing import Nothing
        >>> Just(5).chain(lambda el: Just(el * el))
        Just(25)
        >>> Just(5).chain(lambda _: Nothing)
        Nothing
        >>> Nothing.chain(lambda el: Just(el * el))
        Nothing
        >>> Nothing.chain(lambda _: Nothing)
        Nothing
        """
        return chainer(self.value)

    def __repr__(self) -> str:
        return f'Just({self.value})'

    def alt(self, _alternative: 'Maybe[_T]') -> 'Maybe[_T]':
        """Return the given ``alternative`` if called on a ``Nothing``,
        otherwise the method returns the value it is called on.

        >>> from ._nothing import Nothing
        >>> Just(5).alt(Just(10))
        Just(5)
        >>> Nothing.alt(Just(10))
        Just(10)
        """
        return self

    def alt_lazy(
        self, _maker: t.Callable[[], 'Maybe[_Y]']
    ) -> 'Maybe[t.Union[_Y, _T]]':
        """Return the result of ``maker`` if called on a ``Nothing``, otherwise
        the method returns the value it is called on.

        >>> from ._nothing import Nothing
        >>> Just(5).alt_lazy(lambda: print(10))
        Just(5)
        >>> Nothing.alt_lazy(lambda: [print(10), Just(15)][1])
        10
        Just(15)
        """
        return self

    def unsafe_extract(self) -> _T:
        """Get the value from a ``Just``, or raise if called on a ``Nothing``.

        >>> Just(10).unsafe_extract()
        10
        """
        return self.value

    def or_default_lazy(self, _producer: t.Callable[[], _Y]) -> _T:
        """Get the value from a ``Just``, or return the given a default as
        produced by the given function.

        >>> from ._nothing import Nothing
        >>> Just(5).or_default_lazy(lambda: [print('call'), 10][-1])
        5
        >>> Nothing.or_default_lazy(lambda: [print('call'), 10][-1])
        call
        10
        """
        return self.value

    def or_default(self, _value: _Y) -> _T:
        """Get the value from a ``Just``, or return the given ``default``.

        >>> from ._nothing import Nothing
        >>> Just(5).or_default(10)
        5
        >>> Nothing.or_default(10)
        10
        """
        return self.value

    def case_of(
        self,
        *,
        just: t.Callable[[_T], _TT],
        nothing: t.Callable[[], _TT],  # pylint: disable=unused-argument
    ) -> _TT:
        """A poor mans version of pattern matching.

        >>> from ._nothing import Nothing
        >>> obj1, obj2 = object(), object()
        >>> on_just = lambda el: [print('just', el), obj1][1]
        >>> on_nothing = lambda: [print('nothing'), obj2][1]
        >>> Nothing.case_of(just=on_just, nothing=on_nothing) is obj2
        nothing
        True
        >>> Just(5).case_of(just=on_just, nothing=on_nothing) is obj1
        just 5
        True
        """
        return just(self.value)

    def if_just(self, callback: t.Callable[[_T], object]) -> 'Just[_T]':
        """Call the given callback with the wrapped value if this value is a
        ``Just``, otherwise do nothing.

        >>> from ._nothing import Nothing
        >>> printer = lambda el: print('call', el)
        >>> Nothing.if_just(printer)
        Nothing
        >>> Just(5).if_just(printer)
        call 5
        Just(5)
        """
        callback(self.value)
        return self

    def if_nothing(self, callback: t.Callable[[], object]) -> 'Just[_T]':  # pylint: disable=unused-argument
        """Call the given callback if this value is a ``Nothing``, otherwise do
        nothing.

        >>> from ._nothing import Nothing
        >>> printer = lambda: print('call')
        >>> _ = Just(5).if_nothing(printer)
        >>> _ = Nothing.if_nothing(printer)
        call
        """
        return self

    def try_extract(
        self, _make_exception: t.Union[t.Callable[[], Exception], Exception]
    ) -> _T:
        """Try to extract the value, raising an exception created by the given
        argument if the value is ``Nothing``.

        >>> from ._nothing import Nothing
        >>> Just(5).try_extract(Exception)
        5
        >>> Nothing.try_extract(lambda: Exception())
        Traceback (most recent call last):
        ...
        Exception
        >>> Nothing.try_extract(Exception())
        Traceback (most recent call last):
        ...
        Exception
        """
        return self.value

    def __bool__(self) -> t.NoReturn:
        raise Exception('Do not check Just for boolean value')
