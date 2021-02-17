"""Utilities to translate resources between platforms.

Classes
-------
Translator
    A translator superclass.

Functions
---------
attr
    A translator method decorator for dynamic attributes.
"""

import inspect
from collections.abc import Mapping, Sequence
from operator import attrgetter

from .utils import _nested_update


class Translator:
    """A translator superclass.

    Attributes
    ----------
    resource
        The resource to translate.
    from_map : bool
        If ``True``, `resource` attributes will be indexed by key.
    repr : dict
        The translated resource.
    """

    def __init__(self, resource, from_map=False, **kwargs):
        """
        Parameters
        ----------
        resource
            The resource to translate. By default, attributes are accessed via dot
            notation (see `from_map` below).
        from_map : bool, optional
            If ``True``, `resource` attributes will be indexed by key.
        **kwargs
            Key-value pairs to be set on the translated resource. To set nested
            attributes, pass a mapping (the key will remain the top-level attribute).
            The final key-value pair overwrites.
        """

        self.resource = resource
        self.from_map = from_map
        self.repr = self.constants.copy() if hasattr(self, "constants") else {}

        if hasattr(self, "mapping"):
            self.repr.update(self._add_mapping(self.mapping))

        for attr, meth in filter(
            lambda attr_meth: hasattr(attr_meth[1], "_attr"),
            inspect.getmembers(self, inspect.ismethod),
        ):
            val = meth()

            if val is not None:
                if isinstance(meth._attr, tuple) and meth._attr:
                    nest = self.repr.setdefault(meth._attr[0], {})
                    for key in meth._attr[1:]:
                        nest = nest.setdefault(key, {})
                    nest[attr] = val
                else:
                    self.repr[attr] = val

        _nested_update(self.repr, kwargs)

    def _add_mapping(self, mapping):
        repr = {}

        for attr, val in mapping.items():

            if isinstance(val, str):
                try:
                    pot_val = (
                        self.resource[val]
                        if self.from_map
                        else attrgetter(val)(self.resource)
                    )
                except (KeyError, AttributeError):
                    continue

            elif isinstance(val, Sequence):

                if not self.from_map:
                    raise TypeError(
                        "Sequences are used to fetch nested keys when `from_map` is `True`."
                    )
                elif not val:
                    continue

                pot_val = self.resource

                for key in val:
                    try:
                        pot_val = pot_val[key]
                    except KeyError:
                        pot_val = None
                        break

            elif isinstance(val, Mapping):
                pot_val = self._add_mapping(val) or None

            if pot_val is not None:
                repr[attr] = pot_val

        return repr


def attr(*f_or_keys):
    """A translator method decorator for dynamic attributes.

    The decorated function's name becomes the attribute's key. To create nested
    attributes, pass each higher-level key in order. If not providing keys, it is not
    necessary to call the decorator.

    Parameters
    ----------
    *f_or_keys : callable or str
        If ``str``, ordered keys to create nested attributes.
    """

    if f_or_keys and callable(f_or_keys[0]):
        f_or_keys[0]._attr = True
        return f_or_keys[0]

    def dec(f):
        f._attr = f_or_keys or True
        return f

    return dec


class AbortTranslation(Exception):
    pass
