"""
Utilities 
"""

from dataclasses import Field
from typing import Text
from typing import Type, Union, TypeVar

from pyspark.sql import Column

Columnable = Union[Text, Column, Field]


def get_name(obj):
    if isinstance(obj, str):
        return obj
    if isinstance(obj, property):
        obj = obj.fget
    for att in ["name", "_name", "__name__"]:
        try:
            return getattr(obj, att)
        except:
            ...
    raise ValueError(f"Can not figure out {obj}'s name.")


t_Expected = TypeVar('t_Expected')


class _Empty:
    @staticmethod
    def of(atype: Type[t_Expected]) -> t_Expected:
        return _Empty


class Deffer(object):

    def __init__(self, _tinder: 'TinderBox' = None):
        self._tinder_context = _tinder
        self._parent: Deffer = _Empty.of(Deffer)
        self._value = _Empty

    def propagate_context(self, context):
        self._tinder_context = context
        if self._parent is not _Empty:
            self._parent.propagate_context(context)

    def eval(self, *args, **kwargs):
        if self._value is _Empty:
            if self._parent is not _Empty:
                self._parent = self._unravel(self._parent)
            self._value = self.exec(*args, **kwargs)
        return self._value

    def exec(self, *args, **kwargs):
        raise NotImplementedError()

    def _unravel(self, item):
        return self.unravel(item, self._tinder_context)

    @staticmethod
    def unravel(item, _tinder_context: 'TinderBox' = _Empty):
        if isinstance(item, Deffer):
            if _tinder_context is not _Empty:
                item.propagate_context(_tinder_context)
            return item.eval()
        return item

    # proxying
    # TODO This probably needs to be built out a bit more to cover all special cases (based off some proxies I looked at.)
    def __getattr__(self, item):
        return self.chain(item)

    def __len__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return self.chain("__eq__")(other)

    def chain(self, key):
        _parent = self
        chained = DelayedCall(key, _tinder=self._tinder_context)
        chained._parent = self
        return chained.faux_call


class DelayedCall(Deffer):
    def __init__(self, _callable, *args, _tinder: 'TinderBox' = None, **kwargs):
        super().__init__(_tinder)
        self._callable = _callable
        if len(args) or len(kwargs):
            self.faux_call(*args, **kwargs)

    def faux_call(self, *a, **kw):
        self._args = list(a)
        self._kwargs = kw
        return self

    def exec(self, *a, **kw):
        if isinstance(self._callable, str):
            self._callable = getattr(self.unravel(self._parent), self._callable)
        return self._callable(*(self._unravel(a) for a in self._args),
                              **dict((k, self._unravel(v)) for k, v in self._kwargs.items()))
