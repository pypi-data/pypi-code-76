from sys import getsizeof

import pytest
from jerome.keeper import SymbolKeeper


def test_keeper(printable, k):
    s = next(k)
    assert s not in printable


def test_keep(k):
    s = next(k)
    k.keep(s)
    assert isinstance(k[s], str)
    k.release(s)
    with pytest.raises(KeyError):
        k[s]


def test_size(k):
    s = next(k)
    k.keep(s)
    size = getsizeof(k[s])
    assert 50 <= size <= 76


def test_repr(k):
    s = next(k)
    k.keep(s)
    repr(k[s])


def test_all():
    new_k = SymbolKeeper()
    l = list(new_k)
