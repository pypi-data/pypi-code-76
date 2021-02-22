import dataclasses
import typing as t
from collections.abc import Iterable
from functools import singledispatchmethod
from sys import getsizeof


def get_symbols(
    min_cost: int = 0,
    max_cost: int = 50,
    min_ordinal: int = 0,
    max_ordinal: int = 1114111,
    test: t.Optional[t.Callable[[str], bool]] = lambda x: True,
) -> t.List[str]:
    return (
        chr(i)
        for i in range(min_ordinal, max_ordinal)
        if getsizeof(chr(i)) <= max_cost and test(i)
    )


@dataclasses.dataclass
class SymbolKeeper:
    kept: t.Dict[str, str] = dataclasses.field(default_factory=dict)
    max_cost: int = 76
    reserved: set = dataclasses.field(default_factory=set)

    def __post_init__(self):
        self._symbol_generator = get_symbols(max_cost=76)

    @singledispatchmethod
    def keep(self, symbol) -> None:
        raise ValueError("symbol should be a str or iterable of str or tuples.")

    @keep.register
    def _(self, symbol: str, replacement: str = None):
        self.kept[symbol] = replacement if replacement is not None else next(self)

    @keep.register
    def _(self, symbol: Iterable) -> None:
        [self.keep(c) for c in symbol]

    def release(self, s: str):
        for c in s:
            del self.kept[c]

    def __iter__(self):  # pragma: no cover
        return self

    def __next__(self):
        ch = None
        while ch is None:
            ch = next(
                ch
                for ch in self._symbol_generator
                if ch not in self.reserved
                and ch not in self.kept
                and ch not in "0123456789\003\002\000\001"
            )
        return ch

    def __getitem__(self, character: str) -> str:
        return self.kept[character]


if __name__ == "__main__":
    import string

    k = SymbolKeeper()
    k.keep(
        "a",
    )
    print(k["a"])

    k.keep(list(string.digits))
    print(k["1"])
    print(len(k.kept))