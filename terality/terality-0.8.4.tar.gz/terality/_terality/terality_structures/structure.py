from dataclasses import dataclass
from functools import partial, partialmethod
import sys
from typing import Any, Set, Callable, Optional, Iterable, Type

from . import call_pandas_function


# WARNING: `sys.gettrace` is considered a CPython implementation detail, so we check that it's available.
# See [documentation](https://docs.python.org/3.8/library/sys.html?highlight=gettrace#sys.gettrace).
_process_is_being_debugged: bool = hasattr(sys, "gettrace") and sys.gettrace() is not None


class PandasDisplay:
    min_rows: int = 5
    max_rows: int = 20
    min_cols: int = 5
    max_cols: int = 20


class ClassMethod(type):
    _class_name: str
    _pandas_class: Any
    _additional_class_methods: Set[str] = {'from_pandas'}

    def __getattr__(cls, key: str) -> Callable:
        call = partial(call_pandas_function, cls._class_name, None, key)

        if key in cls._additional_class_methods:
            return call

        # If doesn't have attr, raise with the same error, but TODO erase this step
        type_ = type(getattr(cls._pandas_class, key)).__name__
        if type_ == 'function':
            return call
        raise ValueError(f'Should not be called {key} of type {type_}')

    def __dir__(self) -> Iterable[str]:
        members = list(self._additional_class_methods)
        if self._pandas_class is not None:
            members += list(dir(self._pandas_class))
        return members


class Struct(metaclass=ClassMethod):
    _class_name: str
    _pandas_class_instance: Any = None
    _additional_methods = {'to_pandas', 'load', 'save'}
    _acessors: Set[str] = set()
    _indexers = {'iat', 'at', 'loc', 'iloc'}

    @classmethod
    def _is_method(cls, item):
        return callable(getattr(cls._pandas_class_instance, item))

    def _call(self, accessor: Optional[str], func_name: str, *args, **kwargs):
        return call_pandas_function(self._class_name, accessor, func_name, self, *args, **kwargs)

    def __getattr__(self, item: str):
        if item == '_ipython_display_':
            return partial(self._call_method, None, item, PandasDisplay)
        if item == '__str__' or item == '__repr__':
            return lambda: 'truc'
        if (item.startswith('_') and not item.startswith('__')) or item in ['__class__', '__getattribute__']:
            if item not in ['_repr_html_']:
                return object.__getattribute__(self, item)
        if item in self._cached_attributes:
            return self._cached_attributes[item]
        if item in self._acessors:
            return NameSpace(self, item)
        if item in self._indexers:
            return Indexer(self, item)
        if item in self._additional_methods:
            return partial(self._call, None, item)
        # noinspection PyUnresolvedReferences, PyProtectedMember
        if isinstance(getattr(type(self.__class__)._pandas_class, item), property):
            return self._call(None, item)
        if self._is_method(item):
            return partial(self._call, None, item)
        raise AttributeError(f"'{type(self)}' has no attribute {item!r}")

    ###################################################################################################################
    # Magic methods

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            return self._call(None, '__setattr__', key=key, value=value)

    def __getitem__(self, item):
        return self._call(None, '__getitem__', item=item)

    def __setitem__(self, key, value):
        self._call(None, '__setitem__', key=key, value=value)

    def __delitem__(self, key):
        self._call(None, '__delitem__', key=key)

    def __str__(self):
        # NOTE: When debugging, we avoid network calls and fall back to a bare bones representation.
        if _process_is_being_debugged:
            cls = type(self)
            _id = getattr(self, "_id", None)
            return f'terality.{cls.__name__}(_id={_id})'
        return self._call(None, '__str__')

    def __repr__(self):
        return self.__str__()

    def __dir__(self) -> Iterable[str]:
        # WARNING: When the process is being debugged, we do not want to list any dynamic properties.
        # Why? Because the debugger's variable view uses `dir` to list a variable's children, then evaluates them.
        # Listing dynamic properties would cause spurious calls to the server.
        if _process_is_being_debugged:
            members = [key for key in self.__dict__.keys() | type(self).__dict__.keys()
                       if key.startswith('_') and not key.startswith('__')]
            return members

        members = list(self._additional_methods)
        if self._pandas_class_instance is not None:
            members += list(dir(self._pandas_class_instance))
        return members

    @classmethod
    def _deser(cls, id: str, cached_attributes=None):
        struct = cls.__new__(cls)
        struct._id = id
        struct._cached_attributes = {} if cached_attributes is None else cached_attributes
        return struct

    def _assign(self, other: 'Struct'):
        self._id = other._id
        self._cached_attributes = other._cached_attributes


# Add operators programmatically
# ------------------------------

def _operator(lhs: Struct, rhs: Any, function_name: str):
    # noinspection PyProtectedMember
    return lhs._call(None, function_name, rhs)


def _register_operators():
    # Some operators have a left and right version.
    for function_name in ['add', 'sub', 'mul', 'floordiv', 'truediv', 'pow']:
        for function_variant in [function_name, 'r' + function_name]:
            operator_name = f'__{function_variant}__'
            setattr(Struct, operator_name, partialmethod(_operator, function_name=function_variant))

    # Other operators have only one version:
    for function_name in ['lt', 'le', 'eq', 'ne', 'ge', 'gt']:
        operator_name = f'__{function_name}__'
        setattr(Struct, operator_name, partialmethod(_operator, function_name=function_name))


_register_operators()


@dataclass
class NameSpace:
    _obj: Struct
    name: str

    def __getattr__(self, item: str):
        if item.startswith('_'):
            return object.__getattribute__(self, item)
        # noinspection PyProtectedMember
        return partial(self._obj._call, self.name, 'general', item)


@dataclass
class Indexer:
    obj: Struct
    name: str

    def __getitem__(self, item):
        # noinspection PyProtectedMember
        return self.obj._call(self.name, '__getitem__', item)

    def __setitem__(self, key, value):
        # noinspection PyProtectedMember
        self.obj._call(self.name, '__set_item__', key, value)


@dataclass
class Property:
    name: str

    def __get__(self, obj: Struct, cls: Type[Struct]):
        # noinspection PyProtectedMember
        return obj._call(self.name, '__get__')


class StructIterator:
    def __init__(self, struct: Struct):
        self.struct = struct
        self.size = struct.size
        self.pos = 0
        self.buffer = []
        self.buffer_start = 0

    def __iter__(self):
        # Must return itself, as per the [documentation](https://docs.python.org/3.8/library/stdtypes.html#typeiter).
        return self

    @property
    def buffer_stop(self):
        return self.buffer_start + len(self.buffer)

    def __next__(self) -> Any:
        if self.pos >= self.size:
            raise StopIteration()
        if self.pos >= self.buffer_stop:
            self.buffer_start = self.buffer_stop
            self.buffer = self.struct.get_range_auto(self.buffer_start)
        value = self.buffer[self.pos - self.buffer_start]
        self.pos += 1
        return value
