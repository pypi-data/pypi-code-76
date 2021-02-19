"""ROIs abstract module."""

from copy import copy

from collections import UserDict


class AbstractItem:
    """Abstract item.

    Parameters
    ----------
    key:
        Identification key.
    name: str, optional
        ROI/Category/SubCategory name.
    **kwargs: str, optional
        Region description/Science objective/Observation requirement/Color.

    """

    def __init__(self, key, name=None, **kwargs):
        self.key = key
        self.name = 'Unnamed' if name is None or name == 'None' else name.title()

        self._attrs = kwargs

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return '\n - '.join([
            f'<{self.__class__.__name__}> {self} ({self.name})',
            *[
                f'{k.replace("_", " ").title()}: {v}'
                for k, v in self._attrs.items()
            ]
        ])

    def __eq__(self, other):
        return str(self) == other


class AbstractCollection(UserDict):
    """Abstract collection."""
    ITEM = AbstractItem

    def __repr__(self):
        return '\n - '.join([
            f'<{self.__class__.__name__}> {self.count}',
            *self.data.keys()
        ])

    def __iter__(self):
        """Iterator on values and not keys like regular dict."""
        return iter(self.data.values())

    def __getitem__(self, key):
        if str(key) in self.data:
            return self.data[str(key)]
        raise KeyError(key)

    def __setitem__(self, key, attrs):
        """Add a new item.

        Note
        ----
        If an ``ITEM`` is directely provided, the item
        will be copy an its key will be updated with
        the new one.

        """
        if isinstance(attrs, self.ITEM):
            _item = copy(attrs)
            _item.key = key

            self.data[str(key)] = _item
        else:
            self.data[str(key)] = self.ITEM(key, **attrs)

    @property
    def count(self):
        """Count items."""
        ITEM = self.ITEM.__name__

        n = len(self)
        if n > 1:
            ITEM = (ITEM + 's') if ITEM[-1] != 'y' else (ITEM[:-1] + 'ies')
        if n == 0:
            n = 'No'

        return f'{n} {ITEM.lower()}'

    def keys(self):
        """Keys iterators."""
        return self.data.keys()

    def items(self):
        """Keys and values iterators."""
        return self.data.items()
