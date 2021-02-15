"""This module contains various utils for working with ``Maybe``s.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

from ._just import Just
from ._maybe import Maybe
from ._nothing import Nothing

_S = t.TypeVar('_S')
_T = t.TypeVar('_T')


def merge2(maybe_s: Maybe[_S], maybe_t: Maybe[_T]) -> Maybe[t.Tuple[_S, _T]]:
    """Merge two maybes together in a tuple if both just.

    >>> from . import Just, Nothing
    >>> merge2(Just(5), Just(6))
    Just((5, 6))
    >>> merge2(Nothing, Just(6))
    Nothing
    >>> merge2(Just(6), Nothing)
    Nothing
    """
    return maybe_s.chain(lambda s: maybe_t.map(lambda t: (s, t)))


def from_nullable(val: t.Optional[_T]) -> Maybe[_T]:
    """Covert a nullable to a maybe.

    >>> from_nullable(5)
    Just(5)
    >>> from_nullable(None)
    Nothing
    """
    if val is None:
        return Nothing
    return Just(val)


def maybe_from_nullable(val: t.Union[None, _T, Maybe[_T]]) -> Maybe[_T]:
    """Convert a nullalbe to a maybe if it isn't already a maybe.

    >>> maybe_from_nullable(Just(5))
    Just(5)
    >>> maybe_from_nullable(5)
    Just(5)
    >>> maybe_from_nullable(None)
    Nothing
    >>> maybe_from_nullable(Nothing)
    Nothing
    """
    if isinstance(val, Just):
        return val
    elif Nothing.is_nothing_instance(val):
        return val  # type: ignore
    return from_nullable(val)  # type: ignore
