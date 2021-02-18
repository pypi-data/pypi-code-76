#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""Bapy Package."""
from __future__ import annotations

import ast
import asyncio
import asyncio.events
import asyncio.runners
import atexit
import collections
import collections.abc
import copy
import concurrent.futures
import configparser
import dataclasses
import datetime
import dis
import distutils.command.install
import enum
import errno
import functools
# noinspection PyCompatibility
import grp
import importlib.metadata
import importlib.resources
import inspect
import io
import json
import logging
import logging.handlers
import mailbox
import os
import pathlib
import pickle
import pkgutil
import platform
import pprint
# noinspection PyCompatibility
import pwd
import random
from contextlib import suppress

import retry_decorator
import setuptools
import shlex
import shutil
import site
import socket
import subprocess
import sys
import tempfile
import time
import traceback
import tracemalloc
import types
import typing
import urllib.error
import urllib.request
import warnings
from collections import defaultdict
from collections import OrderedDict
from functools import partial
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Final
from typing import Generic
from typing import Iterable
from typing import Literal
from typing import MutableMapping
from typing import NamedTuple
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import ipaddress
import box
import click
import click_completion
import colorlog
import distro
import dotenv
import dpath.util
import environs
import furl
import git
import icecream
import importlib_metadata
import inflect
import jinja2
import motor.motor_asyncio
import psutil
import pymongo.database
import pymongo.errors
import requests
import rich
import rich.logging
import ruamel
import setuptools.command.develop
import setuptools.command.install
import shell_proc
import shellingham
import sty
import typer
import urllib3
import verboselogs
import xml

import xmltodict
from asgiref.sync import sync_to_async
from decorator import decorate, decorator

urllib3.disable_warnings()

# <editor-fold desc="Typing">
AliasType = typing._alias
CodeType = types.CodeType
datafield = dataclasses.field
FrameInfo = inspect.FrameInfo
FrameType = types.FrameType
GenericAlias = typing._GenericAlias
IPv4Address = ipaddress.IPv4Address
IPv6Address = ipaddress.IPv6Address
Logger = logging.Logger

MongoDBMotor = motor.motor_asyncio.AsyncIOMotorDatabase
MongoDBPy = pymongo.database.Database
MongoDB = Union[MongoDBMotor, MongoDBPy]

MongoClientMotor = motor.motor_asyncio.AsyncIOMotorClient
MongoClientPy = pymongo.MongoClient
MongoClient = Union[MongoClientMotor, MongoClientPy]

MongoColMotor = motor.motor_asyncio.AsyncIOMotorCollection
MongoColPy = pymongo.database.Collection
MongoCol = Union[MongoColMotor, MongoColPy]

MongoCursorMotor = motor.motor_asyncio.AsyncIOMotorCursor
MongoCursorPy = pymongo.cursor.Cursor
MongoCursor = Union[MongoCursorMotor, MongoCursorPy]

MongoValue = Optional[Union[bool, dict, list, str]]
MongoFieldValue = dict[str, MongoValue]

NmapCommandPortTyping = Optional[Union[Literal['-'], str, int]]
NmapCommandScriptTyping = Union[Literal['complete'], str]

Pathlib = pathlib.Path
PathLike = os.PathLike

# </editor-fold>

# <editor-fold desc="Literal">
TasksLiteral = typing.Literal['cancelled', 'finished', 'pending']

# </editor-fold>

# <editor-fold desc="Constants">
all_ports = range(0, 65535)
app = typer.Typer()
console = rich.console.Console()
context = dict(help_option_names=['-h', '--help'], color=True)
cprint = console.print
fm = pprint.pformat
fmi = icecream.IceCreamDebugger(prefix=str()).format
fmt = icecream.IceCreamDebugger(prefix=str(), includeContext=True).format
ic = icecream.IceCreamDebugger(prefix=str())
icc = icecream.IceCreamDebugger(prefix=str(), includeContext=True)
ip_version = {4: dict(af=socket.AF_INET), 6: dict(af=socket.AF_INET6)}
localhost = '127.0.0.1'
os.environ["PYTHONWARNINGS"] = "ignore"


# </editor-fold>

# <editor-fold desc="EnumDict">
class EnumDict(enum.Enum):

    @staticmethod
    def _check_methods(C, *methods):
        # collections.abc._check_methods
        mro = C.__mro__
        for method in methods:
            for B in mro:
                if method in B.__dict__:
                    if B.__dict__[method] is None:
                        return NotImplemented
                    break
            else:
                return NotImplemented
        return True

    @classmethod
    def asdict(cls) -> dict:
        return {key: value._value_ for key, value in cls.__members__.items()}

    @classmethod
    def attrs(cls) -> list:
        return list(cls.__members__)

    @staticmethod
    def auto() -> enum.auto:
        return enum.auto()

    @classmethod
    def default_attr(cls) -> str:
        return cls.attrs()[0]

    @classmethod
    def default_dict(cls) -> dict[str, Any]:
        return {cls.default_attr(): cls.default_value()}

    @classmethod
    def default_value(cls) -> Any:
        return cls[cls.default_attr()]

    @property
    def describe(self) -> tuple:
        """
        Returns:
            tuple:
        """
        # self is the member here
        return self.name, self.value

    @property
    def lower(self) -> str:
        return self.name.lower()

    @property
    def lowerdot(self) -> str:
        return self.value if self.name == 'NO' else f'.{self.name.lower()}'

    def prefix(self, prefix: str) -> str:
        return f'{prefix}_{self.name}'

    @classmethod
    def values(cls) -> list:
        return list(cls.asdict().values())

    @classmethod
    def __subclasshook__(cls, C):
        if cls is EnumDict:
            attrs = [C] + ['asdict', 'attrs', 'auto', 'default_attr', 'default_dict', 'default_value',
                           'describe', 'lower', 'lowerdot', 'prefix', 'values', '_generate_next_value_', '_missing_',
                           'name', 'value', '__members__'] + C.attrs()
            return cls._check_methods(*attrs)
        return NotImplemented


EnumDictType = AliasType(EnumDict, 1, name=EnumDict.__name__)


# </editor-fold>
# <editor-fold desc="EnumDict's">
class AttributeKind(EnumDict):
    CLASS = 'class method'
    DATA = 'data'
    METHOD = 'method'
    PROPERTY = 'property'
    STATIC = 'static method'


class Executor(EnumDict):
    THREAD = concurrent.futures.ThreadPoolExecutor
    PROCESS = concurrent.futures.ProcessPoolExecutor


class GetAll(EnumDict):
    KEYS = EnumDict.auto()
    VALUES = EnumDict.auto()


class ListUtils(EnumDict):
    LOWER = EnumDict.auto()
    UPPER = EnumDict.auto()
    CAPITALIZE = EnumDict.auto()


class LogLevel(EnumDict):
    SPAM = verboselogs.SPAM
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    NOTICE = verboselogs.NOTICE
    WARNING = logging.WARNING
    SUCCESS = verboselogs.SUCCESS
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Nap(EnumDict):
    """
    Nap Helper Class.

    Examples:
        >>> from bapy import Nap
        >>> Nap.lock.sleep()
        >>> asyncio.run(Nap.lock.asleep())
    """
    LOCK = 5
    MONGO = 10
    RAND = 0.1, 2.1,
    QUEUE = 2

    @property
    def time(self) -> Union[int, float]:
        return round(random.uniform(self.value[0], self.value[1]), 2) if isinstance(self.value, tuple) else self.value

    def sleep(self) -> None:
        time.sleep(self.time)

    async def asleep(self) -> None:
        await asyncio.sleep(self.time)


class PathIs(EnumDict):
    DIR = 'is_dir'
    FILE = 'is_file'


class PathMode(EnumDict):
    DIR = 0o666
    FILE = 0o777
    X = 0o755


class PathOption(EnumDict):
    BOTH = EnumDict.auto()
    DIRS = EnumDict.auto()
    FILES = EnumDict.auto()


class PathOutput(EnumDict):
    BOTH = 'both'
    BOX = box.Box
    DICT = dict
    LIST = list
    NAMED = collections.namedtuple
    TUPLE = tuple


class PathSuffix(EnumDict):
    NO = str()
    BASH = EnumDict.auto()
    ENV = EnumDict.auto()
    GIT = EnumDict.auto()
    INI = EnumDict.auto()
    J2 = EnumDict.auto()
    JINJA2 = EnumDict.auto()
    LOG = EnumDict.auto()
    MONGO = EnumDict.auto()
    OUT = EnumDict.auto()
    PY = EnumDict.auto()
    TOML = EnumDict.auto()
    SH = EnumDict.auto()
    YAML = EnumDict.auto()
    YML = EnumDict.auto()


class Priority(EnumDict):
    HIGH = 20
    LOW = 1


# </editor-fold>

# <editor-fold desc="NamedTuple">
Attribute = NamedTuple('Attribute', cls=Type, kind=AttributeKind, object=Any)
CmdOut = NamedTuple('CmdOut', stdout=Union[list, str], stderr=Union[list, str], rc=int)
IPLoc = collections.namedtuple('IPLoc', 'country_name country_code state city postal latitude longitude',
                               defaults=tuple(['Not found'] * 7))
IPv4Named = NamedTuple('IPv4Named', addr=IPv4Address, str=int)
Proto = collections.namedtuple('Protos', 'tcp udp')
ProtoStatus = collections.namedtuple('ProtoStatus', 'ip port proto open')
TasksNamed = collections.namedtuple('TasksNamed', 'cancelled finished pending')

# </editor-fold>
# <editor-fold desc="namedtuple's">
proto_name = Proto(*Proto._fields)
proto_sock = Proto(socket.SOCK_STREAM, socket.SOCK_DGRAM)
tasks_named = TasksNamed(*TasksNamed._fields)


# </editor-fold>

# <editor-fold desc="Decorators">
def _memoize(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args, frozenset(kw.items())
    else:
        key = args
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        cache[key] = func(*args, **kw)
    return cache[key]


def memoize(f):
    """
    A simple memoize implementation. It works by adding a .cache dictionary
    to the decorated function. The cache will grow indefinitely, so it is
    your responsibility to clear it, if needed.
    """
    f.cache = {}
    return decorate(f, _memoize)


def _memonoself(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args[1:], frozenset(kw.items())
    else:
        key = args[1:]
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        cache[key] = func(*args, **kw)
    return cache[key]


def memonoself(f):
    """
    Does not cache and check args[0] -> self
    """
    f.cache = {}
    return decorate(f, _memonoself)


async def _memonoself_aio(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args[1:], frozenset(kw.items())
    else:
        key = args[1:]
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        cache[key] = await func(*args, **kw)
    return cache[key]


def memonoself_aio(f):
    """
    Does not cache and check args[0] -> self
    """
    f.cache = {}
    return decorate(f, _memonoself)


def _memonone(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args, frozenset(kw.items())
    else:
        key = args
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        if (rv := func(*args, **kw)) is None:
            return None
        cache[key] = rv
    return cache[key]


def memonone(f):
    """
    Cache after value has changed from None.
    """
    f.cache = {}
    return decorate(f, _memonone)


def _once(func, *args, **kw):
    # args[0] is self.
    if not func.cache:
        func.cache = func(*args, **kw)
    return func.cache


def once(f):
    """
    A simple memoize implementation. It works by adding a .cache dictionary
    to the decorated function. The cache will grow indefinitely, so it is
    your responsibility to clear it, if needed.
    """
    f.cache = None
    return decorate(f, _once)


# </editor-fold>

# <editor-fold desc="dict_sort, get_setuptools_script_dir, pop_default & upper_prefix">
def dict_sort(name: dict, ordered: bool = False) -> Union[dict, collections.OrderedDict]:
    """
    Order a dict based on keys.

    Args:
        name: dict to be ordered.
        ordered: OrderedDict

    Returns:
        Union[dict, collections.OrderedDict]:
    """
    rv = {key: name[key] for key in sorted(name)}
    if ordered:
        return collections.OrderedDict(rv)
    return rv


class OnlyGetScriptPath(distutils.command.install.install):
    def run(self):
        # does not call install.run() by design
        # noinspection PyUnresolvedReferences
        self.distribution.install_scripts = self.install_scripts


def get_setuptools_script_dir():
    dist = setuptools.Distribution({'cmdclass': {'install': OnlyGetScriptPath}})
    dist.dry_run = True  # not sure if necessary, but to be safe
    dist.parse_config_files()
    command = dist.get_command_obj('install')
    command.ensure_finalized()
    command.run()
    return dist.install_scripts


def pop_default(data: dict, key: Any, default: Any = None) -> tuple[Any, dict]:
    """
    Dict Pop with Default.

    Examples:
        >>> pop_default(dict(a=1), 'b', True) #doctest: +ELLIPSIS
        (True, {'a': 1})
        >>> pop_default(dict(a=1), 'b') #doctest: +ELLIPSIS
        (None, {'a': 1})
        >>> pop_default(dict(a=1), 'a') #doctest: +ELLIPSIS
        (1, {})

    Args:
        data: data
        key: key
        default: default

    Returns:
        tuple[Any, dict]:
    """
    try:
        value = data.pop(key)
    except KeyError:
        value = default
    return value, data


def upper_prefix(data: Union[dict, list, set, str, tuple] = None, *, prefix: str = None,
                 envs: environs.Env = None) -> Optional[Union[dict, list, set, str, tuple]]:
    """
    Dict/List/Tuple Upper Items/Keys and Prefix Add.

    Examples:
        >>> upper_prefix()
        >>> pfx = 'repo'
        >>> tests = {'first': 1, 'second': 2}
        >>> upper_prefix(prefix=pfx)
        'REPO_'
        >>> upper_prefix(tests)
        {'FIRST': 1, 'SECOND': 2}
        >>> upper_prefix(tests, prefix=pfx)
        {'REPO_FIRST': 1, 'REPO_SECOND': 2}
        >>> data_new = tuple(tests.keys())
        >>> upper_prefix(data_new, prefix=pfx)
        ('REPO_FIRST', 'REPO_SECOND')
        >>> data_new = list(tests.keys())
        >>> upper_prefix(data_new, prefix=pfx)
        ['REPO_FIRST', 'REPO_SECOND']
        >>> upper_prefix('first', prefix=pfx)
        'REPO_FIRST'

    Args:
        data: data to upper and to add prefix.
        prefix: prefix to add.
        envs: `environs.Env` file.

    Returns:
        Optional[Union[dict, list, set, str, tuple]]:
    """

    def get_prefix(v: str):
        p = f'{prefix.upper()}_' if prefix and not prefix.endswith('_') else prefix
        return f'{p.upper()}{v.upper()}' if prefix else v.upper()

    if data is None and prefix and envs is None:
        return get_prefix(str())
    if isinstance(data, dict):
        return {get_prefix(key): value for key, value in data.items()}
    else:
        for item in (list, set, tuple):
            if isinstance(data, item):
                if envs is None:
                    return item(get_prefix(var) for var in data)
                else:
                    return {var: envs(get_prefix(var), None) for var in data}
        if isinstance(data, str):
            return get_prefix(data)


# </editor-fold>

# <editor-fold desc="Obj">
_Obj = TypeVar('_Obj')


@dataclasses.dataclass
class Obj(Generic[_Obj]):
    data: Any
    depth: Optional[int] = None
    prop: bool = False
    swith: str = '__'

    __exclude_attr__ = []  # Exclude instance attribute.
    __exclude_convert__ = True  # True for instance repr instead of nested asdict.
    __exclude_copy__ = [environs.Env, git.Remote, ]  # Exclude copy.deepcopy.

    @property
    def copy(self):
        for cls in self.asdict_exclude_copy:
            if isinstance(self.data, cls):
                print(self.data, cls)
                return self.data

        try:
            new = copy.deepcopy(self.data)
        except (copy.error, pickle.PickleError, ):
            if hasattr(self.data, 'copy'):
                new = self.data.copy()
            else:
                new = self.data
        return new

    @property
    def get_class(self) -> Any:
        return self.data if self.is_class else type(self.data)

    @property
    def get_module(self) -> Any:
        return inspect.getmodule(self.data)

    @property
    def get_mro(self) -> tuple:
        return self.data.__mro__ if self.is_class and self.has_mro else self.get_class.__mro__ \
            if self.new(self.get_class).has_mro else tuple()

    @property
    def get_vars(self) -> dict:
        return vars(self.data) if self.has_dict else dict()

    @property
    def get_vars_class(self) -> dict:
        return self.new(self.get_class).get_vars

    @property
    def has_mro(self) -> bool:
        return hasattr(self.data, '__mro__')

    @property
    def has_dict(self) -> bool:
        return hasattr(self.data, '__dict__')

    @property
    def is_bool(self) -> bool:
        if self.is_int:
            return isinstance(self.data, bool)
        return False

    @property
    def is_bytes(self) -> bool:
        return isinstance(self.data, bytes)

    @property
    def is_callable(self) -> bool:
        return isinstance(self.data, Callable)

    @property
    def is_class(self) -> bool:
        return inspect.isclass(self.data)

    @property
    def is_dataclass(self) -> bool:
        return self.is_class and dataclasses.is_dataclass(self.data)

    @property
    def is_dataclass_instance(self) -> bool:
        return not self.is_class and hasattr(type(self.data), dataclasses._FIELDS)

    @property
    def is_defaultdict(self) -> bool:
        return isinstance(self.data, defaultdict)

    @property
    def is_dict(self) -> bool:
        return isinstance(self.data, dict)

    @property
    def is_dlst(self) -> bool:
        return any([isinstance(self.data, item) for item in [dict, list, set, tuple]])

    @property
    def is_end(self) -> bool:
        return self.is_str and self.data.endswith(self.swith)

    @property
    def is_float(self) -> bool:
        return isinstance(self.data, float)

    @property
    def is_int(self) -> bool:
        return isinstance(self.data, int)

    @property
    def is_iterable(self) -> bool:
        return isinstance(self.data, Iterable)

    @property
    def is_list(self) -> bool:
        return isinstance(self.data, list)

    @property
    def is_lst(self) -> bool:
        return any([isinstance(self.data, item) for item in [list, set, tuple]])

    @property
    def is_mlst(self) -> bool:
        return any([isinstance(self.data, item) for item in [MutableMapping, list, set, tuple]])

    @property
    def is_module(self) -> bool:
        return inspect.ismodule(self.data)

    @property
    def is_mutablemapping(self) -> bool:
        return isinstance(self.data, MutableMapping)

    @property
    def is_namedtuple(self) -> bool:
        return not self.is_class and self.is_tuple and hasattr(self.data, '_asdict')

    @property
    def is_obj_dict(self):
        return not self.is_class and self.has_dict and not self.is_namedtuple

    @property
    def is_ordereddict(self) -> bool:
        return isinstance(self.data, OrderedDict)

    @property
    def is_routine(self) -> bool:
        return inspect.isroutine(self.data)

    @property
    def is_set(self) -> bool:
        return isinstance(self.data, set)

    @property
    def is_start(self) -> bool:
        return self.is_str and self.data.startswith(self.swith)

    @property
    def is_str(self) -> bool:
        return isinstance(self.data, str)

    @property
    def is_tuple(self) -> bool:
        return isinstance(self.data, tuple)

    def _asdict(self, count: int = 1) -> Union[dict, Any]:
        if self.is_lst:
            obj = type(self.data)(v for v in self.data if self.asdict_include(value=v))
        elif self.is_namedtuple:
            obj = self.asdict_namedtuple
        elif self.is_obj_dict:
            obj = self.asdict_kind_data | self.asdict_kind_properties
        elif self.is_mutablemapping:
            obj = self.asdict_mutablemapping
        else:
            return self.copy

        rv = dict() if self.is_mutablemapping else list()
        for key in obj.data:
            value = obj.data.get(key)
            if self.depth is None or count < self.depth:
                value = self.new(value)._asdict(count=count + 1)
            rv[key] = self.new(value).copy
            rv.update({key: value}) if self.is_mutablemapping else rv.append(value)
        rv = rv if self.is_mutablemapping else type(obj.data)(rv)
        return rv

    @property
    def asdict(self) -> dict:
        return self._asdict

    @property
    def asdict_exclude_attr(self) -> list:
        return sorted({
            attr for item in [*self.get_mro, type(self)]
                       for attr in getattr(item, '__exclude_attr__', type(self.__exclude_attr__)())
        }.update(self.new(self).class_attrs(AttributeKind.PROPERTY)))

    def asdict_exclude_convert(self, value: Any) -> Any:
        if hasattr(self.data, '__exclude_convert__') and getattr(self.data, '__exclude_convert__', False):
            return r if (r := repr(value)) else str(value)
        return value

    @property
    def asdict_exclude_copy(self) -> list:
        return list({attr for item in [*self.get_mro, type(self)]
                     for attr in getattr(item, '__exclude_copy__', type(self.__exclude_copy__)())})

    @property
    def asdict_excluded(self) -> Optional[bool]:
        return any([self.get_module == typing, self.is_module, self.is_routine,
                    self.is_class, self.is_start])

    def asdict_include(self, key: Any = None, value: Any = None) -> Optional[bool]:
        if key:
            ic(key)
            return key not in self.asdict_exclude_attr and not self.new(key).asdict_excluded
        if value:
            ic(value)
            return not self.new(value).asdict_excluded

    @property
    def asdict_kind_data(self) -> dict:
        if self.is_obj_dict:
            return {k: self.asdict_exclude_convert(v) for k, v in (self.get_vars_class | self.get_vars).items() if k in
                    self.class_attrs(AttributeKind.DATA) and self.asdict_include(k) and self.asdict_include(value=v)}
        return dict()

    @property
    def asdict_kind_properties(self) -> dict:
        rv = dict()
        if self.is_obj_dict:
            for prop in self.class_attrs(AttributeKind.PROPERTY):
                if self.asdict_include(prop):
                    with warnings.catch_warnings(record=False):
                        warnings.filterwarnings('ignore', category=RuntimeWarning)
                        warnings.showwarning = lambda *_args, **_kwargs: None
                        value = getattr(self.data, prop)
                    if self.asdict_include(value):
                        rv |= {prop: self.asdict_exclude_convert(value)}
        return rv

    @property
    def asdict_mutablemapping(self) -> dict:
        return {k: self.asdict_exclude_convert(v) for k, v in (self.data if self.is_mutablemapping else dict()).items()
                if self.asdict_include(k) and self.asdict_include(value=v)}

    @property
    def asdict_namedtuple(self) -> dict:
        return {k: self.asdict_exclude_convert(v) for k, v in (
            self.data._asdict() if self.is_namedtuple else dict()).items()
                if self.asdict_include(k) and self.asdict_include(value=v)}

    def class_attrs(self, kind: Optional[AttributeKind] = None) -> Optional[Union[dict[str, Attribute], list]]:
        """
        Class attrs info.

        Examples:
            >>> from bapy import Path, AttributeKind, Obj
            >>> Obj(Path).class_attrs()
            >>> Obj(Path).class_attrs(AttributeKind.DATA)
            >>> Obj(Path, swith='_').class_attrs(AttributeKind.PROPERTY)

        Args:
            kind: return attrs kind list instead of dict with all.

        Returns:
            Optional[Union[dict[str, Attribute], list]]:
        """
        if kind:
            return [item.name for item in inspect.classify_class_attrs(self.get_class) if item.kind == kind.value]
        return {item.name: Attribute(item.defining_class, AttributeKind[iter_split(item.kind)[0].upper()],
                                     item.object) for item in inspect.classify_class_attrs(self.get_class)}

    def new(self, data: Any, /, **kwargs) -> _Obj:
        # noinspection PyArgumentList
        return type(self)(**vars(self) | dict(data=data) | kwargs)


# </editor-fold>

# <editor-fold desc="dict_sort, get_setuptools_script_dir, pop_default & upper_prefix">
def dict_sort(name: dict, ordered: bool = False) -> Union[dict, collections.OrderedDict]:
    """
    Order a dict based on keys.

    Args:
        name: dict to be ordered.
        ordered: OrderedDict

    Returns:
        Union[dict, collections.OrderedDict]:
    """
    rv = {key: name[key] for key in sorted(name)}
    if ordered:
        return collections.OrderedDict(rv)
    return rv


class OnlyGetScriptPath(distutils.command.install.install):
    def run(self):
        # does not call install.run() by design
        # noinspection PyUnresolvedReferences
        self.distribution.install_scripts = self.install_scripts


def get_setuptools_script_dir():
    dist = setuptools.Distribution({'cmdclass': {'install': OnlyGetScriptPath}})
    dist.dry_run = True  # not sure if necessary, but to be safe
    dist.parse_config_files()
    command = dist.get_command_obj('install')
    command.ensure_finalized()
    command.run()
    return dist.install_scripts


def pop_default(data: dict, key: Any, default: Any = None) -> tuple[Any, dict]:
    """
    Dict Pop with Default.

    Examples:
        >>> pop_default(dict(a=1), 'b', True) #doctest: +ELLIPSIS
        (True, {'a': 1})
        >>> pop_default(dict(a=1), 'b') #doctest: +ELLIPSIS
        (None, {'a': 1})
        >>> pop_default(dict(a=1), 'a') #doctest: +ELLIPSIS
        (1, {})

    Args:
        data: data
        key: key
        default: default

    Returns:
        tuple[Any, dict]:
    """
    try:
        value = data.pop(key)
    except KeyError:
        value = default
    return value, data


def upper_prefix(data: Union[dict, list, set, str, tuple] = None, *, prefix: str = None,
                 envs: environs.Env = None) -> Optional[Union[dict, list, set, str, tuple]]:
    """
    Dict/List/Tuple Upper Items/Keys and Prefix Add.

    Examples:
        >>> upper_prefix()
        >>> pfx = 'repo'
        >>> tests = {'first': 1, 'second': 2}
        >>> upper_prefix(prefix=pfx)
        'REPO_'
        >>> upper_prefix(tests)
        {'FIRST': 1, 'SECOND': 2}
        >>> upper_prefix(tests, prefix=pfx)
        {'REPO_FIRST': 1, 'REPO_SECOND': 2}
        >>> data_new = tuple(tests.keys())
        >>> upper_prefix(data_new, prefix=pfx)
        ('REPO_FIRST', 'REPO_SECOND')
        >>> data_new = list(tests.keys())
        >>> upper_prefix(data_new, prefix=pfx)
        ['REPO_FIRST', 'REPO_SECOND']
        >>> upper_prefix('first', prefix=pfx)
        'REPO_FIRST'

    Args:
        data: data to upper and to add prefix.
        prefix: prefix to add.
        envs: `environs.Env` file.

    Returns:
        Optional[Union[dict, list, set, str, tuple]]:
    """

    def get_prefix(v: str):
        p = f'{prefix.upper()}_' if prefix and not prefix.endswith('_') else prefix
        return f'{p.upper()}{v.upper()}' if prefix else v.upper()

    if data is None and prefix and envs is None:
        return get_prefix(str())
    if isinstance(data, dict):
        return {get_prefix(key): value for key, value in data.items()}
    else:
        for item in (list, set, tuple):
            if isinstance(data, item):
                if envs is None:
                    return item(get_prefix(var) for var in data)
                else:
                    return {var: envs(get_prefix(var), None) for var in data}
        if isinstance(data, str):
            return get_prefix(data)


# </editor-fold>

# <editor-fold desc="AsDict, DataProxy & NameDefault">
class AsDict:
    """Dict and Attributes Tuple Class."""
    __asdict_exclude__ = ['asdict', 'asdict_keys', 'public', '__obj__', ]

    def __obj__(self, swith: str = Obj.swith) -> Obj:
        return Obj(self, prop=True, swith=swith)

    @property
    def asdict(self) -> dict:
        """
        Dict including properties without routines.

        Returns:
            dict:
        """
        return self.__obj__().asdict

    @property
    def asdict_keys(self) -> list:
        """
        Return a Tuple with instances attributes names.

        Returns:
            list:
        """
        return sorted(list(self.asdict.keys()))

    @classmethod
    def attrs(cls) -> list:
        if dataclasses.is_dataclass(cls):
            # noinspection PyDataclass
            return sorted([field.name for field in dataclasses.fields(cls)])

    @classmethod
    def defaults(cls, ordered: bool = False) -> Union[dict, collections.OrderedDict]:
        if dataclasses.is_dataclass(cls):
            # noinspection PyDataclass
            return dict_sort({field.name: field.default for field in dataclasses.fields(cls)}, ordered)

    def post_init_default(self, cls: Any = None, type_index: int = 0):
        """Sets value of field to index of field type: `typing.Union[dict, str, NoneType]`."""
        if dataclasses.is_dataclass(cls):
            for field in dataclasses.fields(cls):
                if getattr(self, field.name) == field.default:
                    setattr(self, field.name, field.type.__args__[type_index]())

    @property
    def public(self) -> dict:
        """
        Dict including properties without routines.

        Returns:
            dict:
        """
        return self.__obj__(swith='_').asdict

    @property
    def values(self) -> list:
        return list(self.asdict.values())


class DataProxy:
    """Dict+Attr Get/Set Data Proxy Helper Class."""

    def attrs_get(self, *args, **kwargs) -> dict:
        """
        Get One or More Attributes.

        Examples:
            >>> dataproxy = DataProxy()
            >>> dataproxy.d1 = 1
            >>> dataproxy.d2 = 2
            >>> dataproxy.d3 = 3
            >>> assert dataproxy.attrs_get('d1') == {'d1': 1}
            >>> assert dataproxy.attrs_get('d1', 'd3') == {'d1': 1, 'd3': 3}
            >>> assert dataproxy.attrs_get('d1', 'd4', default=False) == {'d1': 1, 'd4': False}

        Raises:
            ValueError: ValueError

        Args:
            *args: attr(s) name(s).
            **kwargs: default.

        Returns:
            dict:
        """
        if not args:
            raise ValueError(f'args must be provided.')
        default = kwargs.get('default', None) if kwargs else None
        return {item: getattr(self, item, default) for item in args}

    def attrs_set(self, *args, **kwargs) -> Any:
        """
        Sets one or more attributes.

        Examples:
            >>> dataproxy = DataProxy()
            >>> dataproxy.attrs_set(d_1=31, d_2=32)
            >>> dataproxy.attrs_set('d_3', 33)
            >>> d_4_5 = dict(d_4=4, d_5=5)
            >>> dataproxy.attrs_set(d_4_5)
            >>> dataproxy.attrs_set('c_6', 36, c_7=37)
            >>> assert Obj(dataproxy).asdict == {'c_6': 36, 'c_7': 37, 'd_1': 31, 'd_2': 32, 'd_3': 33, 'd_4': 4,
            ... 'd_5': 5}


        Raises:
            ValueError: ValueError

        Args:
            *args: attr name and value.
            **kwargs: attrs names and values.
        """
        if args:
            if len(args) > 2 or (len(args) == 1 and not isinstance(args[0], dict)):
                raise ValueError(f'args, invalid args length: {args}. One dict or two args (var name and value.')
            kwargs.update({args[0]: args[1]} if len(args) == 2 else args[0])

        for key, value in kwargs.items():
            setattr(self, key, value)


@dataclasses.dataclass
class NameDefault:
    name: Optional[str] = str()
    default: Any = str()


@dataclasses.dataclass
class Nested:
    """
    Nested delete keys or values in dict and decode objects.

    Examples:
        >>> v = {'open': { 'ip': {1: 'http'}, 'sctp': {}, \
                          'tcp': {80: {'open': True, 'script': {}, 'service': 'http'}, \
                                  443: {'open': True, 'script': {}, 'service': 'https'} }, 'udp': {} }}
        >>> assert not dpath.util.search(Nested(v, 0, 'service').run(), '**/service')
        >>> assert not dpath.util.search(Nested(v, 0, values='http').run(), '**', afilter=lambda x: 'http' == x)
        >>> assert not dpath.util.search(Nested(v, 0, 'service', \
            values='http').run(), '**', afilter=lambda x: 'http' == x)

    Returns:
        dict:
    """
    obj: Any = datafield(default_factory=dict)
    depth: int = 1
    keys: Union[Callable, Iterable] = lambda x: False  # Iterable of callable which returns True if delete.
    values: Union[Callable, Iterable] = lambda x: False  # values: Iterable of callable which returns True if delete.
    count: int = datafield(default=0, init=False)
    _keys: set = datafield(default_factory=set, init=False)
    _values: set = datafield(default_factory=set, init=False)

    def __post_init__(self):
        if isinstance(self.keys, Iterable):
            self._keys = set(iter_split(self.keys))

        if isinstance(self.values, Iterable):
            self._values = set(iter_split(self.values))

        self.run()

    @staticmethod
    def copy(data):
        if hasattr(data, 'copy'):
            new = data.copy()
        else:
            new = data
        return new

    def exclude(self, data: Any, key: bool = True) -> Optional[bool]:
        if isinstance(self.keys if key else self.values, Iterable):
            for item in self._keys if key else self._values:
                if data == item:
                    return True
        elif isinstance(self.keys if key else self.values, Callable):
            return self.keys(data) if key else self.values(data)
        # elif self.keys is None and key:
        #     return False
        # elif self.values is None and not key:
        #     return False

    def run(self, data: Any = None) -> dict:
        data = data if data else self.obj
        cls = getattr(data, '__class__')
        not_path = not isinstance(data, Path)

        with warnings.catch_warnings(record=False):
            warnings.filterwarnings('ignore', category=RuntimeWarning)
            warnings.showwarning = lambda *_args, **_kwargs: None
            if isinstance(data, tuple) and hasattr(data, '_asdict'):
                return self.run(data._asdict())
            elif dataclasses.is_dataclass(data):
                return self.run(dataclasses.asdict(data))
            elif hasattr(data, '__dict__') and cls and not_path:
                obj_value = vars(data)
                obj_cls_dict = vars(cls)
                # Add class attributes not in obj attributes.
                obj_cls_value = {k: v for k, v in obj_cls_dict.items() if k not in obj_value}
                cls_attrs = {}
                return self.run({key: value for key, value in (obj_cls_value | obj_value).items() if key in cls_attrs})
            elif isinstance(data, (MutableMapping, list, set, tuple)):
                mapping = isinstance(data, MutableMapping)
                rv = dict() if mapping else list()
                for item in data:
                    value = data.get(item) if mapping else item
                    if (self.depth and self.count < self.depth) or not self.depth:
                        self.count += 1
                        excl_values = (self.values and self.exclude(value, False)) \
                            if mapping else (self.keys and self.exclude(item))
                        if not ((self.keys and self.exclude(item)) or excl_values):
                            value_cls = hasattr(value, '__class__')
                            value_not_path = not isinstance(value, Path)
                            if isinstance(value, (MutableMapping, list, set, tuple)) \
                                    or (dataclasses.is_dataclass(data)) \
                                    or (hasattr(value, '__dict__') and value_cls and value_not_path):
                                value = self.run(value)
                            else:
                                if hasattr(value, 'text'):
                                    value = getattr(value, 'text')

                    rv.update({item: self.copy(value)}) if mapping else rv.append(self.copy(value))
                    if not mapping:
                        type(data)(rv)
                self.count = -1
                return rv


# </editor-fold>

# <editor-fold desc="Classes and Data: No deps (.. Distro, Executable, Machine .. Url)">
class AliasedGroup(click.Group):
    """
    Implements execution of the first partial match for a command. Fails with a
    message if there are no unique matches.

    See: https://click.palletsprojects.com/en/7.x/advanced/#command-aliases.
    """

    def get_command(self, ctx, cmd_name: str):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@dataclasses.dataclass
class Distro:
    """Distro Class."""
    _info: Any = collections.namedtuple('LinuxDistribution', tuple(distro.LinuxDistribution().info().keys()),
                                        defaults=tuple(distro.LinuxDistribution().info().values()))()
    _id: str = _info.id
    _codename: str = _info.codename
    _like: str = _info.like
    _distro_version_parts: Any = collections.namedtuple('DistroVersionParts', tuple(_info.version_parts.keys()),
                                                        defaults=tuple(_info.version_parts.values()))()
    _version_parts_major: int = int(_distro_version_parts.major)
    _version_parts_minor: int = int(_distro_version_parts.minor)
    _version_parts_build_number: Union[int, str] = int(_distro_version_parts.build_number) \
        if _distro_version_parts.build_number else str()
    CENTOS: bool = True if _id == 'centos' else False
    centos_codenames: tuple = ('Core', 'Final',)
    CENTOS_CORE: bool = True if _codename == 'Core' else False
    CENTOS_FINAL: bool = True if _codename == 'Final' else False
    centos_releases: tuple = ('8', '7', '6',)
    CENTOS_8: bool = True if _version_parts_major == '8' else False
    CENTOS_7: bool = True if _version_parts_major == '7' else False
    CENTOS_6: bool = True if _version_parts_major == '6' else False
    DEBIAN: bool = True if _id == 'debian' else False
    debian_codenames: tuple = ('bookworm', 'bullseye', 'buster', 'stretch',)
    DEBIAN_BOOKWORM: bool = True if _codename == 'bookworm' else False
    DEBIAN_BULLSEYE: bool = True if _codename == 'bullseye' else False
    DEBIAN_BUSTER: bool = True if _codename == 'buster' else False
    DEBIAN_STRETCH: bool = True if _codename == 'stretch' else False
    DEBIAN_LIKE: bool = True if _like == 'debian' or _id == 'debian' else False
    FEDORA: bool = True if _id == 'fedora' else False
    fedora_codenames: tuple = ('',)
    FEDORA_LIKE: bool = \
        True if _like == 'fedora' or _id == 'fedora' or 'fedora' in _like else False
    fedora_releases: tuple = ('33', '32',)
    FEDORA_33: bool = True if _version_parts_major == '33' else False
    FEDORA_32: bool = True if _version_parts_major == '32' else False
    KALI: bool = True if _id == 'kali' else False
    MACOS: bool = psutil.MACOS
    macos_codenames: tuple = ('',)
    POSIX: bool = psutil.POSIX
    RHEL: bool = True if _id == 'rhel' else False
    rhel_codenames: tuple = ('Ootpa', 'Maipo',)
    RHEL_LIKE: bool = True if 'rhel' in _like else False
    rhel_releases: tuple = ('8', '7',)
    RHEL_8: bool = True if _version_parts_major == '8' else False
    RHEL_7: bool = True if _version_parts_major == '7' else False
    UBUNTU: bool = True if _id == 'ubuntu' else False
    ubuntu_codenames: tuple = ('focal', 'bionic', 'xenial',)
    UBUNTU_FOCAL: bool = True if _codename == 'focal' else False
    UBUNTU_BIONIC: bool = True if _codename == 'bionic' else False
    UBUNTU_XENIAL: bool = True if _codename == 'xenial' else False
    kernel: str = _id  # darwin (macOS), linux (redhat, ubuntu) - os.uname().sysname is capitalized
    kernels: tuple = ('darwin', 'linux',)
    KERNEL_AIX: bool = psutil.AIX
    KERNEL_BSD: bool = psutil.BSD
    KERNEL_FREEBSD: bool = psutil.FREEBSD
    KERNEL_DARWIN: bool = True if _id == 'darwin' else False
    KERNEL_LINUX: bool = psutil.LINUX
    KERNEL_NETBSD: bool = psutil.NETBSD
    KERNEL_OPENBSD: bool = psutil.OPENBSD
    KERNEL_SUNOS: bool = psutil.SUNOS
    KERNEL_WINDOWS: bool = psutil.WINDOWS
    build: int = _version_parts_build_number
    codename: str = _codename
    distro: str = _id
    distros: tuple = ('centos', 'darwin', 'debian', 'fedora', 'rhel', 'ubuntu',)
    like: str = _like  # centos is like 'rhel fedora'
    likes: tuple = ('debian', 'fedora', 'rhel fedora',)
    major: int = _version_parts_major
    minor: int = _version_parts_minor
    version: str = _info.version  # macOS (19.5.0), Ubuntu (16.04), rhel (8.2)

    @classmethod
    def exec(cls, name) -> bool:
        """
        Checks if executable is in ``PATH``.

        Args:
            name: executable/command name.

        Returns:
            bool:
        """
        return True if shutil.which(name) is not None else False

    @classmethod
    def install(cls, name, cask: bool = False) -> str:
        """
        Installs package.

        Args:
            name: executable/command name.
            cask: brew cask.

        Raises:
            NotImplementedError: Not installer.
            FileNotFoundError: Not in PATH after install.

        Returns:
            Str:
        """
        brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/install.sh'
        if not cls.exec(name):
            if cls.MACOS:
                if not cls.exec('brew'):
                    out_cmd = cmd(f'yes yes | /bin/bash -c "$(curl -fsSL {brew_url})" ')
                    if out_cmd.rc != 0:
                        raise NotImplementedError(f'package not available {name}.')
                options = 'cask' if cask else str()
                command = f'brew {options} install'
            elif cls.DEBIAN_LIKE or cls.KALI:
                command = f'apt install -y'
            elif cls.FEDORA_LIKE:
                command = f'yum install -y'
            else:
                raise NotImplementedError('Not installer available.')

            out_cmd = cmd(f'{command} {name}')
            if out_cmd.rc != 0:
                red(fm(out_cmd.stderr))

        if cls.exec(name):
            return shutil.which(name)
        raise FileNotFoundError(f'{name} not in PATH.')


@dataclasses.dataclass
class Executable(AsDict):
    apt: Union[Distro.exec, str] = 'apt'
    brew: Union[Distro.exec, str] = 'brew'
    curl: Union[Distro.exec, str] = 'curl'
    docker: Union[Distro.exec, str] = 'docker'
    go: Union[Distro.exec, str] = 'go'
    haproxy: Union[Distro.exec, str] = 'haproxy'
    make: Union[Distro.exec, str] = 'make'
    nmap: Union[Distro.exec, str] = 'nmap'
    npm: Union[Distro.exec, str] = 'npm'
    pip: Union[Distro.exec, str] = 'pip'
    pip3: Union[Distro.exec, str] = 'pip3'
    r: Union[Distro.exec, str] = 'r'
    yum: Union[Distro.exec, str] = 'yum'

    def __post_init__(self):
        self.post_init_default(Executable)


class Enum(enum.Enum):
    @classmethod
    def new(cls, name, attrs: Iterable, doc: str = str(), start: Any = 1,
            default: int = 0) -> Union[Type[enum.Enum], Iterable]:
        """
        Creates a new enum.

        # Examples:
        #     >>> from bapy import DataProxy, Executor, ExitCode, Extend, ListUtils, LogR, Path, Meta
        #     >>> Enum.new('ApiVersion', 'v1 beta', doc='Nexus API version')
        #     <enum 'ApiVersion'>
        #     >>> Enum.new('ApiVersion', 'v1 beta', doc='Nexus API version').default
        #     <ApiVersion.v1: 1>
        #     >>> Executor.asdict
        #     {'NONE': 1, 'THREAD': 2, 'PROCESS': 3}
        #     >>> ExitCode.default
        #     <ExitCode.LARGE_FILE_ERROR: 100>
        #     >>> assert DataProxy in Extend.ALL.value
        #     >>> ListUtils.attrs
        #     ('LOWER', 'UPPER', 'CAPITALIZE', 'PREFIX', 'SUFFIX')
        #     >>> LogR.Levels.asdict
        #     {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
        #     >>> LogR.Levels.DEBUG.describe
        #     ('DEBUG', 10)
        #     >>> PathMode.__doc__
        #     'Group/Other File/Dir PathMode'
        #     >>> PathMode['FILE']
        #     <PathMode.FILE: 511>
        #     >>> PathOption.FILES
        #     <PathOption.FILES: 'files'>
        #     >>> Path.Output.NAMED.value
        #     'named'

        Args:
            name: name
            attrs: field names
            doc: docstring
            start: True ``name.lower()``, False ``name``. object getattr(start, name), Tuple values like methods, et.
            default: default

        Returns:
            Type[Enum]:
        """
        new_cls = Enum(name, attrs, start=start)
        if isinstance(start, tuple):
            new_cls.values = start
        new_cls.__doc__ = doc if doc else f'{name} Enum'
        new_cls.asdict = {key: value._value_ for key, value in new_cls.__members__.items()}
        new_cls.attrs = tuple(new_cls.__members__)
        new_cls.default = new_cls[new_cls.attrs[default]]
        return new_cls

    def _generate_next_value_(self, start, count, last_values):
        if isinstance(start, bool):
            if start:
                return self.lower()
            else:
                return self
        elif isinstance(start, int):
            for last_value in reversed(last_values):
                try:
                    return last_value + 1
                except TypeError:
                    pass
            else:
                return start
        elif isinstance(start, tuple):
            return start[count]
        else:
            return getattr(start, str(self))

    @property
    def describe(self) -> tuple:
        """
        Returns:
            tuple:
        """
        # self is the member here
        return self.name, self.value


ExitCode = Enum.new('ExitCode', 'LARGE_FILE_ERROR HTTP_REQUEST_ERROR INVALID_CREDENTIALS_ERROR '
                                'GET_NOT_FOUND_404_ERROR JSON_DECODER_RESPONSE_ERROR INVALID_REPO_PATH_ERROR '
                                'FILE_OR_DIR_ERROR UPLOAD_INVALID_REPO_ERROR UPLOAD_DIR_TO_FILE_ERROR '
                                'SHOW_INVALID_REPO_ERROR LS_UNKNOWN_OR_PATH_ERROR '
                                'UP_DOWN_COUNT_0_ERROR UP_DOWN_API_ERROR UNKNOWN_ERROR API_ERROR SUBCOMMAND_ERROR '
                                'DOWNLOAD_ERROR CONFIG_ERROR ADMIN_CREDENTIALS_NEEDED CONNECTION_ERROR '
                                'DELETE_RESPONSE_ERROR INVALID_ENVIRONMENT_ERROR INVALID_API_VERSION_ERROR '
                                'INVALID_LOG_DIR_ERROR INVALID_LOG_LEVEL_ERROR INVALID_SSH_KEY_FILE_ERROR '
                                'INVALID_CONFIG_FIELD_ERROR INVALID_CONFIG_ATTR_ERROR INVALID_CONFIG_SET_ATTR_ERROR '
                                'INVALID_CONFIG_ERROR', 'Error codes returned by :lib:mod:`repo.cli.cli`.', 100)


class EnvInterpolation(configparser.BasicInterpolation):
    """
    Extended Interpolation which expands environment variables in values.

    Examples:
        >>> import os
        >>> os.environ['PATH_TEST'] = System.exe_path.text
        >>> cfg = '''
        ...     [section]
        ...     key = value
        ...     my_path = ${PATH_TEST}:/private/tmp
        ... '''
        >>>
        >>> config = configparser.ConfigParser(interpolation=EnvInterpolation())
        >>> config.read_string(cfg)
        >>> my_path = config['section']['my_path']
        >>> if my_path == f'{System.exe_path.text}:/private/tmp':
        ...     print(True)
        True
    """

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)

    @staticmethod
    def read_ini(p: PathLike, raw: bool = True) -> Union[configparser.RawConfigParser, configparser.ConfigParser]:
        """
        Read ini with :class:'~configparser.RawConfigParser` or :class:`EnvInterpolation`.

        Args:
            p: path.
            raw: raw.

        Returns:
            Union[configparser.RawConfigParser, configparser.ConfigParser]:
        """
        if raw:
            i = configparser.RawConfigParser()
            i.optionxform = str
        else:
            i = configparser.ConfigParser(interpolation=EnvInterpolation())

        i.read(str(p))
        return i


class IPBase(AsDict, DataProxy, ipaddress._BaseAddress):

    @property
    def text(self):
        return self.exploded


class IPv4(IPv4Address, IPBase):

    def __init__(self, ip, loc: Union[IPLoc, bool] = False, log: LogR = None):
        super().__init__(ip)
        # noinspection PyArgumentList
        self.loc = loc if isinstance(loc, IPLoc) else (iploc(ip) if loc else IPLoc())
        self.log = log if log else _log


class IPv6(IPv6Address, IPBase):

    def __init__(self, ip, loc: Union[IPLoc, bool] = False, log: LogR = None):
        super().__init__(ip)
        # noinspection PyArgumentList
        self.loc = loc if isinstance(loc, IPLoc) else (iploc(ip) if loc else IPLoc())
        self.log = log if log else _log


IPvType = Union[IPv6, IPv4]
IPAddressLike = Union[IPv4, IPv6, IPv4Address, IPv6Address, str, bytes]


@dataclasses.dataclass
class Machine:
    """Server OS and Platform Class."""
    fqdn: str = socket.getfqdn()
    hostname: str = os.uname().nodename.split('.')[0]  # pro, repo
    machine: str = os.uname().machine  # x86_64
    nodename: str = os.uname().nodename  # pro, repo.nferx.com
    processor: str = platform.processor()  # amdk6,


class PostDevelopCommand(setuptools.command.develop.develop):
    """Post-installation for development mode."""
    function = None

    def run(self):
        if self.function:
            self.function()
        setuptools.command.develop.develop.run(self)


class PostInstallCommand(setuptools.command.install.install):
    """Post-installation for installation mode."""
    function = None

    def run(self):
        if self.function:
            self.function()
        setuptools.command.install.install.run(self)


class Up:
    """APP/CLI PathOption."""
    Bump: Any = Literal['patch', 'minor', 'major']

    @classmethod
    def args(cls):
        return cls.Bump.__args__

    @classmethod
    def option(cls):
        return typer.Option(cls.args()[0], help='Version part to be increased.', autocompletion=cls.args)


class Url(furl.furl):
    """
    Furl Class.

    GitHub repositories http
    GitHub repos ssh
    Go
    Api Rest
    Repo test and prod
    Ports and Docker host

    Examples:
        >>> assert Url.email(os.environ.get('USER')) == Url.email(User.name)
        >>> Url.github()
        Url('https://github.com')
        >>> Url.wiki(number=183238657, page='Hola')
        Url('https://nferx.atlassian.net/wiki/spaces/DevOps/pages/183238657/Hola')
        >>> Url.lumenbiomics(repo='test')
        'org-4379404@github.com:lumenbiomics/test'
        >>> http_url = Url.lumenbiomics(http=True, repo='test', username=User.github_username, password='password')
        >>> url = f'{Url.scheme_default}://{User.github_username}:password@{Url.github().host}/{Url.organization}/test'
        >>> assert http_url.url == url
        >>> repo = Url(host=Url.nferx(), name='repotest', bind=9091)
        >>> repo.url
        'https://repotest.nferx.com'
        >>> url = Url(host=repo, name='nexus', port=8080, bind=3001)
        >>> url.url, url.name, url.bind
        ('https://nexus.repotest.nferx.com:8080', 'nexus', 3001)
    """
    Domain: Any = collections.namedtuple('Domain', 'nference nferxops nferx')
    domain: Domain = Domain('nference.net', 'nferxops.net', 'nferx.com')
    bind: int = None
    company: str = domain.nference
    container: int = None
    group: str = 'DevOps'
    id: str = 'org-4379404'
    ops: str = domain.nferxops
    organization: str = 'lumenbiomics'
    scheme_default: str = 'https'
    server: str = domain.nferx

    def __init__(self, host: Union[str, furl.furl, Url], name: str = None, **kwargs):
        if not kwargs.get('scheme', None):
            kwargs.update(scheme=self.scheme_default)
        self.bind, kwargs = pop_default(kwargs, 'bind')
        self.container, kwargs = pop_default(kwargs, 'container')
        host = host.host if isinstance(host, Url) else host
        prefix = f'{name}.' if name else str()
        kwargs.update(host=f'{prefix}{host.host if isinstance(host, Url) else host}')
        super(Url, self).__init__(**kwargs)

    @staticmethod
    @app.command(context_settings=context)
    def email(username: str = str(), stdout: bool = False) -> str:
        """
        User Email.

        Args:
            username: username.
            stdout: stdout.

        Returns:
            Str:
        """
        username = username if username else User.name
        rv = f'{username}@{Url.nference().host}'
        if stdout:
            console.print(rv)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def github(stdout: bool = False) -> Url:
        """
        GitHub Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url('github.com')
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def lumenbiomics(http: bool = False, username: str = None, password: str = None,
                     repo: str = None, suffix: bool = False, stdout: bool = False) -> Union[Url, str]:
        """
        Lumenbiomics repos url.

        Args:
            http: http
            username: username
            password: GitHub API token
            repo: repo
            suffix: suffix
            stdout: stdout.

        Returns:
            Any:
        """
        repo = repo if repo else _path_installed.name
        password = password if password else Url.token()
        g = PathSuffix.GIT.lowerdot if suffix else str()
        p = '/'.join((Url.organization, repo)) + g

        if http:
            # https://jose-nferx:<api_token>@github.com/lumenbiomics/configs.git
            rv = Url(Url.github(), **dict(path=f'{p}', **(
                dict(username=username, password=password) if password and username else dict())))
            if stdout:
                console.print(rv.url)
            return rv
        rv = f'{Url.id}@{Url.github().host}:{p}'  # org-4379404@github.com:lumenbiomics/repos.git
        if stdout:
            console.print(rv)
        return rv

    @property
    def name(self) -> str:
        """
        Last path or first subdomain.

        Returns:
            Str:
        """
        return self.path.split('/')[-1] if self.path else self.host.split('.')[0]

    @staticmethod
    @app.command(context_settings=context)
    def nference(stdout: bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.company)
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def nferx(stdout: bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.server)
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def nferxops(stdout: bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.ops)
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def repo(stdout: bool = False) -> Url:
        """
        Repo Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(host=Url.nferx(), name='repo')
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def repository(stdout: bool = False) -> Url:
        """
        Repository repo Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url.repo() / 'repository'
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def repotest(stdout: bool = False) -> Url:
        """
        Repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(host=Url.nferx(), name='repotest')
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def repositorytest(stdout: bool = False) -> Url:
        """
        Repository repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url.repotest() / 'repository'
        if stdout:
            console.print(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def token(stdout: bool = False) -> Url:
        """
        Repository repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = os.environ.get('NFERX_GITHUB_PASSWORD', str())
        if stdout:
            console.print(rv)
        return rv

    @staticmethod
    @app.command(context_settings=context)
    def wiki(space: str = group, number: int = int(), page: str = str(), stdout: bool = True) -> Url:
        """
        Confluence Wiki Url.

        https://nferx.atlassian.net/wiki/spaces/DevOps/pages/183238657/Repository+Manager

        Args:
            space: space
            number: number
            page: page
            stdout: stdout

        Returns:
            Any:
        """
        name = Url.nferx().name
        p = f'wiki/spaces/{space}/pages/{number}/{page.replace(" ", "+")}' if number and page else 'wiki'
        rv = Url('atlassian.net', name=name, path=p)
        if stdout:
            console.print(rv.url)
        return rv


# </editor-fold>

# <editor-fold desc="Path">
class Path(Pathlib, pathlib.PurePosixPath, AsDict, DataProxy):
    """
    Path Helper Class.

    Examples:
        # >>> from bapy import System
        # >>> os.chdir('/usr/local')
        # >>> path = Path('/usr/local').parent
        # >>> path.text, path.str, path.resolved, path.cwd()
        # ('/usr', '/usr', Path('/usr'), Path('/usr/local'))
        # >>> path.cd(System.sys_site)  # cd to new path
        # Path('/usr/local/lib/python3.8/site-packages')
        # >>> path.cd()  # cd to previous
        # Path('/usr/local')
        # >>> path_new = path.cd(System.sys_site)
        # >>> path_new
        # Path('/usr/local/lib/python3.8/site-packages')
        # >>> path_previous = path_new.cd()
        # >>> path_previous
        # Path('/usr/local')
        # >>> path_mkdir_add_test = Path('/tmp').mkdir_add('path_mkdir_add_test')
        # >>> assert '/tmp/path_mkdir_add_test' in path_mkdir_add_test.text
        # >>> path_touch_add_test = Path('/tmp').touch_add('path_touch_add_test')
        # >>> assert '/tmp/path_touch_add_test' in path_touch_add_test.text
        # >>> for glob_test in Path('/tmp').rglob('path*'):
        # ...     glob_test
        # Path('/tmp/path_mkdir_add_test')
        # Path('/tmp/path_touch_add_test')
        # >>> path_mkdir_add_test.rmdir()
        # >>> os.remove(path_touch_add_test.text)
        # >>>
        # >>> from bapy import User
        # >>> Path('/tmp/templates').rm()
        # >>> test = Path('/tmp').mkdir_add('templates') / 'test.templates'
        # >>> test.write_text('Defaults: {{ User.name }} !logfile, !syslog') #doctest: +ELLIPSIS
        # 43
        # >>> Path('/tmp').templates['test'].dump(dest='/tmp/sudoers')
        # >>> Path('/tmp/sudoers').read_text() #doctest: +ELLIPSIS
        # 'Defaults:... !logfile, !syslog'
        # >>> Path('/tmp/templates').rm()
        # >>> Path('/tmp/sudoers').rm()
    """
    cd_: Path = None
    scripts_suffix: bool = False

    __asdict_exclude__ = ['_cached_cparts', 'endseparator', 'requirements', 'scripts', 'scripts_relative', 'str',
                          'templates', ]

    @dataclasses.dataclass
    class J2:
        """Jinja2 Templates Helper Class."""
        src: Path
        data: dict = None
        dest: Union[Path, str] = None
        name: str = datafield(init=False)
        stream: Any = datafield(init=False)
        render: Any = datafield(init=False)

        def __init__(self, src: Path, data: dict = None, dest: Union[Path, str] = None):
            self.src = src
            self.name = src.stem
            self.stream = jinja2.Template(self.src.read_text(), autoescape=True).stream
            self.render = jinja2.Template(self.src.read_text(), autoescape=True).render
            self.data = self.get_data(data)
            self.dest = self.get_dest(dest)

        @staticmethod
        def get_data(variables: dict = None) -> dict:
            f = Frame()
            return variables if variables else {**f.back_globals, **f.back_locals}

        def get_dest(self, dest: Union[Path, str] = None) -> Path:
            return Path(dest) if dest else _path_installed.work.mkdir_add(self.__class__.__name__.lower()) / self.name

        def dump(self, data: dict = None, dest: Union[Path, str] = None):
            self.stream(self.get_data(data)).dump(self.get_dest(dest).text)

    def append_text(self, data, encoding=None, errors=None):
        """
        Open the file in text mode, append to it, and close the file.
        """
        if not isinstance(data, str):
            raise TypeError('data must be str, not %s' %
                            data.__class__.__name__)
        with self.open(mode='a', encoding=encoding, errors=errors) as f:
            return f.write(data)

    def cd(self, p: Any = '-') -> Path:
        """
        Change working dir, returns new Path and stores previous.

        Args:
            p: path

        Returns:
            Path:
        """
        if self.cd_ is None:
            self.cd_ = self.cwd()
        p = self.cd_ if p == '-' else p
        cd_ = self.cwd()
        os.chdir(Path(str(p)).text)
        p = self.cwd()
        p.cd_ = cd_
        return p

    def description(self) -> str:
        """
        Create README.md for project.

        Returns:
            Str:
        """
        readme = self.readme()
        try:
            return readme.splitlines()[0].strip('# ')
        except IndexError as exc:
            _log.error(f'Invalid first line {exc} for README.md: {readme}')
            return str()

    @property
    def endseparator(self) -> str:
        """
        Add trailing separator at the end of path if does not exist.

        Returns:
            Str: path with separator at the end.
        """
        return self.text + os.sep

    def find_up(self, file: PathIs = PathIs.FILE, name: Union[str, PathSuffix] = PathSuffix.ENV,
                previous: bool = False) -> Optional[Union[Path, tuple[Optional[Path], Optional[Path]]]]:
        """
        Find file or dir up.

        Args:
            file: file.
            name: name.
            previous: if found return also previous path.

        Returns:
            Optional[Union[Path, tuple[Optional[Path], Optional[Path]]]:
        """
        name = name if isinstance(name, str) else name.lowerdot
        start = self if self.is_dir() else self.parent
        before = self
        while True:
            find = start / name
            if getattr(find, file.value)():
                if previous:
                    return find, before
                return find
            before = start
            start = start.parent
            if start == Path('/'):
                if previous:
                    return None, None
                return

    def fd(self, *args, **kwargs):
        return os.open(self.text, *args, **kwargs)

    def mkdir_add(self, name, mode=0o700, parents=True, exist_ok=True) -> Path:
        """
        Add directory, make directory and return new Path.

        Args:
            name: name
            mode: mode
            parents: parents
            exist_ok: exist_ok

        Returns:
            Path:
        """
        if not (p := (self / name).resolved).is_dir():
            p.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
        return p

    @property
    def pwd(self) -> Path:
        return self.cwd().resolved

    def readme(self) -> str:
        """
        Create or Read README.md for project.

        Returns:
            Path:
        """
        readme = self / 'README.md'
        if not readme.is_file():
            readme.write_text(f'# {self.name.capitalize()}')
            _log.debug(f'README.md created: {readme}')
        return readme.read_text()

    # noinspection PydanticTypeChecker
    @property
    def requirements(self) -> dict:
        """
        Scans for requirements files and returns a dict with parsed requirements per requirement file.

        Returns:
            dict: dict with parsed requirements per requirement file.
        """
        try:  # for pip >= 10
            # noinspection PyCompatibility
            from pip._internal.req import parse_requirements
        except ImportError:  # for pip <= 9.0.3
            # noinspection PyUnresolvedReferences
            from pip.req import parse_requirements

        # noinspection PydanticTypeChecker,PyTypeChecker
        return {item.stem: [str(req.requirement) for req in parse_requirements(item.text, session='workaround')]
                for item in self.glob('requirements*')}

    @property
    def resolved(self) -> Path:
        return self.resolve()

    def rm(self, missing_ok=True):
        """
        Delete a folder/file (even if the folder is not empty)

        Args:
            missing_ok: missing_ok
        """
        if not missing_ok and not self.exists():
            raise
        if self.exists():
            # It exists, so we have to delete it
            if self.is_dir():  # If false, then it is a file because it exists
                shutil.rmtree(self)
            else:
                self.unlink()

    def scan(self, option: PathOption = PathOption.FILES,
             output: PathOutput = PathOutput.BOX, suffix: PathSuffix = PathSuffix.NO,
             level: bool = False, hidden: bool = False, frozen: bool = False) -> Union[box.Box, dict, list]:
        """
        Scan Path.

        Args:
            option: what to scan in path.
            output: scan return type.
            suffix: suffix to scan.
            level: scan files two levels from path.
            hidden: include hidden files and dirs.
            frozen: frozen box.

        Returns:
            Union[box.Box, dict, list]: list [paths] or dict {name: path}.
        """

        def scan_level():
            b = box.Box()
            for level1 in self.iterdir():
                if not level1.stem.startswith('.') or hidden:
                    if level1.is_file():
                        if option is PathOption.FILES:
                            b[level1.stem] = level1
                    else:
                        b[level1.stem] = {}
                        for level2 in level1.iterdir():
                            if not level2.stem.startswith('.') or hidden:
                                if level2.is_file():
                                    if option is PathOption.FILES:
                                        b[level1.stem][level2.stem] = level2
                                else:
                                    b[level1.stem][level2.stem] = {}
                                    for level3 in level2.iterdir():
                                        if not level3.stem.startswith('.') or hidden:
                                            if level3.is_file():
                                                if option is PathOption.FILES:
                                                    b[level1.stem][level2.stem][level3.stem] = level3
                                            else:
                                                b[level1.stem][level2.stem][level3.stem] = {}
                                                for level4 in level3.iterdir():
                                                    if not level3.stem.startswith('.') or hidden:
                                                        if level4.is_file():
                                                            if option is PathOption.FILES:
                                                                b[level1.stem][level2.stem][level3.stem][level4.stem] \
                                                                    = level4
                                                if not b[level1.stem][level2.stem][level3.stem]:
                                                    b[level1.stem][level2.stem][level3.stem] = level3
                                    if not b[level1.stem][level2.stem]:
                                        b[level1.stem][level2.stem] = level2
                        if not b[level1.stem]:
                            b[level1.stem] = level1
            return b

        def scan_dir():
            both = box.Box({Path(item).stem: Path(item) for item in self.glob(f'*{suffix.lowerdot}')
                            if not item.stem.startswith('.') or hidden})
            if option is PathOption.BOTH:
                return both
            if option is PathOption.FILES:
                return box.Box({key: value for key, value in both.items() if value.is_file()})
            if option is PathOption.DIRS:
                return box.Box({key: value for key, value in both.items() if value.is_dir()})

        rv = scan_level() if level else scan_dir()
        if output is PathOutput.LIST:
            return list(rv.values())
        if frozen:
            return rv.frozen
        return rv

    @property
    def scripts(self) -> list:
        if self.name == 'scripts':
            scripts = self
        else:
            scripts = self / 'scripts'

        if scripts.is_dir():
            _permissions = []
            _ = [item.chmod(PathMode.X.value) for item in scripts.iterdir() if scripts.is_dir()]
            if self.scripts_suffix:
                return [item for item in scripts.iterdir() if item.suffix.endswith(PathSuffix.BASH.lowerdot)
                        or item.suffix.endswith(PathSuffix.SH.lowerdot)]
            return [item for item in scripts.iterdir()]
        return list()

    @property
    def scripts_relative(self) -> list:
        scripts = self.scripts
        return [(item.relative_to(_path_installed.project)).text for item in scripts] if scripts else list()

    @property
    def str(self) -> str:
        return self.text

    @property
    def templates(self) -> dict:
        """
        Iter dir for templates and create dict with name and dump func

        Returns:
            dict:
        """
        if self.name != 'templates':
            # noinspection PyMethodFirstArgAssignment
            self /= 'templates'

        if self.is_dir():
            return {item.stem: self.J2(item) for item in self.glob(f'*.{PathSuffix[self.J2.__name__].lowerdot}')}
        return dict()

    def touch_add(self, name, mode=0o600, exist_ok=True) -> Path:
        """
        Add file, touch and return new Path.

        Args:
            name: name
            mode: mode
            exist_ok: exist_ok

        Returns:
            Path:
        """
        if (p := (self / name).resolved).is_file() is False:
            p.touch(mode=mode, exist_ok=exist_ok)
        return p

    @property
    def text(self):
        return str(self)


CallerVars = NamedTuple('CallerVars', glob=dict, loc=dict)
Caller = NamedTuple('Caller', args=dict, code=list, coro=Optional[bool], file=Path,
                    func=Optional[Union[Callable, property]], funcname=str, glob=dict, loc=dict, lineno=int,
                    module=Optional[str], name=str, package=str, qual=Optional[str],
                    task=str, vars=CallerVars)


def caller(index: int = 2, _vars: bool = True, _glob: bool = False, _loc: bool = False,
           depth: int = Nested.depth) -> Caller:
    """
    1: self, 2: caller, 3: caller back
    Args:
        index: index.
        _vars: _vars.
        _glob: _glob.
        _loc: _loc.
        depth: depth.

    Returns:
        Caller:
    """
    index_init = index

    def has(data: dict, name: str) -> tuple[Optional[bool], Optional[Union[Callable, property]], Optional[str]]:
        def get(func):
            return any([inspect.isawaitable(func), inspect.iscoroutinefunction(func), inspect.isasyncgenfunction(func),
                        inspect.isasyncgen(func)]), func, getattr(func, f'__qualname__')

        with warnings.catch_warnings(record=False):
            warnings.filterwarnings('ignore', category=RuntimeWarning)
            warnings.showwarning = lambda *_args, **_kwargs: None
            if index_init != 1:
                for item in ['self', 'cls']:
                    if obj := data.get(item):
                        if name in dir(obj):
                            if item == 'self':
                                obj_cls = getattr(obj, '__class__')
                                if isinstance(getattr(obj_cls, name), property):
                                    _coro = inspect.isawaitable(getattr(obj, name))
                                    try:
                                        _qual = eval(f'obj.{name}.__qualname__')
                                        return _coro, None, _qual
                                    except AttributeError:
                                        pass
                                else:
                                    return get(getattr(obj, name))
                            else:
                                return get(getattr(obj, name))
                if function := data.get(name):
                    return get(function)
            return None, None, None

    try:
        frame = frame_b = inspect.stack()[index]
    except IndexError:
        index -= 1
        frame = frame_b = inspect.stack()[index]

    try:
        frame_b_b = inspect.stack()[index + 1]
    except IndexError:
        frame_b_b = frame

    if 'asyncio' in frame_b.filename:
        frame = frame_b_b
    if 'asyncio' in frame_b_b.filename:
        frame = frame_b
    inf = inspect.getargvalues(frame.frame)
    args = {name: inf.locals[name] for name in inf.args} | (
        {inf.varargs: val} if (val := inf.locals.get(inf.varargs)) else dict()) | (
               kw if (kw := inf.locals.get(inf.keywords)) else dict())
    loc = frame.frame.f_locals.copy() if 'asyncio' not in frame.filename else dict()
    glob = frame.frame.f_globals.copy() if 'asyncio' not in frame.filename else dict()
    file = Path(frame.filename)
    coro, func_obj, qual = has(glob | loc, frame.function)

    return Caller(del_key(args), frame.code_context, coro, file, func_obj, frame.function, glob if _glob else dict(),
                  loc if _loc else dict(), frame.lineno, inspect.getmodulename(file.text), glob.get('__name__', str()),
                  glob.get('__package__', str()), qual, asyncio.current_task().get_name() if aioloop() else str(),
                  CallerVars(Nested(glob, depth, '', '').run(), Nested(loc, depth, '', '').run())
                  if _vars else CallerVars(dict(), dict()))


PathLike.register(Path)
UnionPaths = Union[PathLike, Pathlib, Path]
UnionPathsStr = Union[PathLike, Pathlib, Path, str]
UnionPathStr = Union[Path, str]
OptionalPath = Optional[Path]
OptionalPaths = Optional[UnionPaths]
OptionalPathStr = Optional[UnionPathStr]
FinalPath = Final[Path]

# </editor-fold>

# <editor-fold desc="User">
try:
    user_actual_name = Path('/dev/console').owner() if psutil.MACOS else os.getlogin()
except OSError:
    user_actual_name = Path('/proc/self/loginuid').owner()


@dataclasses.dataclass
class UserActual:
    """User Base."""
    name: str = user_actual_name
    passwd: Any = datafield(default=pwd.getpwnam(name), init=False)
    gecos: Any = datafield(default=passwd.default.pw_gecos, init=False)
    gid: Any = datafield(default=passwd.default.pw_gid, init=False)
    gname: Any = datafield(default=grp.getgrgid(gid.default).gr_name, init=False)
    home: Any = datafield(default=Path(passwd.default.pw_dir), init=False)
    id: Any = datafield(default=passwd.default.pw_uid, init=False)
    shell: Any = datafield(default=Path(passwd.default.pw_shell), init=False)
    ssh: Any = datafield(default=home.default / '.ssh', init=False)
    id_rsa: Any = datafield(default=ssh.default / 'id_rsa', init=False)
    id_rsa_pub: Any = datafield(default=ssh.default / 'id_rsa.pub', init=False)
    auth_keys: Any = datafield(default=ssh.default / 'authorized_keys', init=False)
    git_config_path: Any = datafield(default=home.default / '.gitconfig', init=False)
    git_config: Any = datafield(default=git.GitConfigParser(git_config_path.default.text), init=False)
    github_username: Any = datafield(default=git_config.default.get_value(section='user', option='username',
                                                                          default=str()), init=False)
    GITHUB_USERNAME: Any = True if github_username else False

    def __post_init__(self):
        try:
            self.passwd = pwd.getpwnam(self.name)
        except KeyError:
            red(f'Invalid user: {self.name}')
        else:
            self.gecos = self.passwd.pw_gecos
            self.gid = self.passwd.pw_gid
            self.gname = grp.getgrgid(self.gid).gr_name
            self.home = Path(self.passwd.pw_dir)
            self.id = self.passwd.pw_uid
            self.shell = Path(self.passwd.pw_shell)
            self.ssh = self.home / '.ssh'
            self.id_rsa = self.ssh / 'id_rsa'
            self.id_rsa_pub = self.ssh / 'id_rsa.pub'
            self.auth_keys = self.ssh / 'authorized_keys'
            self.git_config_path = self.home / '.gitconfig'
            self.git_config = git.GitConfigParser(self.git_config_path.text)
            self.github_username = self.git_config.get_value(section='user', option='username', default=str())
            self.GITHUB_USERNAME = True if self.github_username else False


@dataclasses.dataclass
class UserProcess:
    """User Process Class."""
    sudo_user: str = os.getenv('SUDO_USER')
    SUDO: bool = True if sudo_user is not None else False
    gid: int = os.getgid()
    gname: str = grp.getgrgid(gid).gr_name
    id: int = os.getuid()
    passwd: pwd.struct_passwd = pwd.getpwuid(id)
    gecos: str = pwd.getpwuid(id).pw_gecos
    home: Path = Path(pwd.getpwuid(id).pw_dir)
    name: str = pwd.getpwuid(id).pw_name
    shell: Path = Path(pwd.getpwuid(id).pw_shell)
    ssh: Path = home / '.ssh'
    id_rsa: Path = ssh / 'id_rsa'
    id_rsa_pub: Path = ssh / 'id_rsa.pub'
    auth_keys: Path = ssh / 'authorized_keys'
    ROOT: bool = True if id == 0 else False
    git_config_path = home / '.gitconfig'
    git_config: git.GitConfigParser = git.GitConfigParser(git_config_path.text)
    github_username: str = git_config.get_value(section='user', option='username', default=str())
    GITHUB_USERNAME: bool = True if github_username else False


@dataclasses.dataclass
class User:
    """User Class."""
    username: str = 'upload'
    admin: Any = collections.namedtuple('UserNamed', 'username password', defaults=(
        'admin', os.environ.get('REPO_DEFAULT_ADMIN_PASSWORD', str())))
    default: Any = admin(username, username)
    actual: Final[UserActual] = UserActual()
    process: Final[UserProcess] = UserProcess()
    ROOT: bool = process.ROOT
    SUDO: bool = process.SUDO
    sudo_user: str = process.sudo_user
    passwd: pwd.struct_passwd = process.passwd if SUDO else actual.passwd
    gecos: str = process.gecos if SUDO else actual.gecos
    gid: int = process.gid if SUDO else actual.gid
    gname: str = process.gname if SUDO else actual.gname
    home: Path = process.home if SUDO else actual.home
    id: int = process.id if SUDO else actual.id
    name: str = process.name if SUDO else actual.name
    shell: Path = process.shell if SUDO else actual.shell
    ssh: Path = process.ssh if SUDO else actual.ssh
    id_rsa: Path = process.id_rsa if SUDO else actual.id_rsa
    id_rsa_pub: Path = process.id_rsa_pub if SUDO else actual.id_rsa_pub
    auth_keys: Path = process.auth_keys if SUDO else actual.auth_keys
    git_config_path: Path = process.git_config_path if SUDO else actual.git_config_path
    git_config: git.GitConfigParser = process.git_config if SUDO else actual.github_username
    github_username: str = process.github_username if SUDO else actual.github_username
    GITHUB_USERNAME: bool = process.GITHUB_USERNAME if SUDO else actual.GITHUB_USERNAME


# </editor-fold>

# <editor-fold desc="PathInstalled">
_imported = False
try:
    _module_name = inspect.stack()[1].frame.f_globals.get('__name__')
    _filename = Path(inspect.stack()[1].filename).resolved
    if _module_name in ['importlib._bootstrap', ]:
        _sys_filename = Path(sys.argv[0]).resolved
        if 'PyCharm' not in _sys_filename.text:
            _filename = _sys_filename
        _imported = True
except IndexError:
    _filename = Path(__file__).resolved

PathInstalled = NamedTuple('InstalledPath', filename=Path, home=Path, installed=bool, log_dir=Path, log_file=Path,
                           mongo=Path, name=str, path=Path, prefix=str, project=Path, repo=str, work=Path)


def path_installed(filename: Path) -> PathInstalled:
    installed = False
    project = None
    p = Path(filename.parent)
    name = repo = p.name
    if filename.is_relative_to(Path(get_setuptools_script_dir())):
        installed = True
        repo = name = filename.name
        d = importlib.import_module(name)
        filename = Path(d.__file__)
        # noinspection PyUnresolvedReferences
        p = Path(importlib.resources.files(name))
    else:
        for s in set(site.getsitepackages() + [site.USER_SITE] + [f for f in sys.path if f.endswith('packages')]):
            if filename.is_relative_to(Path(s)):
                installed = True
                relative_to = filename.relative_to(Path(s))
                repo = name = relative_to.parts[0]
                p = Path(s) / name
                break
        if not installed:
            if (found := filename.find_up(file=PathIs.DIR, name=PathSuffix.GIT, previous=True)) == \
                    (None, None,):
                if (found := filename.find_up(file=PathIs.DIR, name='setup.py', previous=True)) == (None, None,):
                    found = (filename, filename)
            project = found[0].parent
            repo = project.name
            p = found[1] if found[1].is_dir() else found[1].parent
            name = p.name
            if 'importlib._bootstrap' in found[1].text:
                import setuptools
                packages = setuptools.find_packages()
                name = repo
                if packages:
                    name = repo if repo in packages else packages[0]
                p = project / name
    home = User.home
    work = home.mkdir_add(f'.{name}')
    log_dir = work.mkdir_add('log')
    prefix = f'{name.upper()}_'
    p.attrs_set(package=p, repo=repo, project=project, installed=installed, prefix=prefix, work=work)

    return PathInstalled(filename, home, installed, log_dir, log_dir.touch_add(f'{name}{PathSuffix.LOG.lowerdot}'),
                         home.touch_add(PathSuffix.MONGO.lowerdot), name, p, prefix, project, repo, work)


_path_installed = path_installed(_filename)


# </editor-fold>

# <editor-fold desc="Frame">
class Frame:
    """Convenience Frame and Stack Class."""
    ctx: int = 1
    index: int = 1

    def __init__(self, index: int = index, ctx: int = ctx):
        frameinfo: FrameInfo = inspect.stack(ctx)[index]
        frame: FrameType = frameinfo.frame
        self.frame = frame
        self.code_context: list = frameinfo.code_context
        self.function: str = frameinfo.function
        self.lineno: int = frameinfo.lineno
        self.filename: Path = Path(frameinfo.filename).resolved

        self.parent: Path = self.filename.parent
        self.module: str = inspect.getmodulename(self.filename.text)

        self.f_code: CodeType = frame.f_code
        self.f_lineno = frameinfo.frame.f_lineno
        self.globals = frame.f_globals

        self.locals = inspect.currentframe().f_locals

        self.package: str = self.globals.get('__package__', None)
        self.globals_name: str = self.globals.get('__name__', None)
        self.globals_file: Path = Path(self.globals.get('__file__', None)).resolved

        self.globals_file_parent: Path = self.globals_file.parent
        self.globals_file_module: str = inspect.getmodulename(self.globals_file.text)

        self.locals_name: str = self.locals.get('__name__', None)

        if back := getattr(frame, 'f_back', None):
            if 'importlib._bootstrap' in str(back):
                if frame_back := getattr(back, 'f_back', None) is not None:
                    frame = frame_back
            self.back = getattr(frame, 'f_back', None)

            self.back_code: CodeType = back.f_code
            self.back_lineno: CodeType = back.f_lineno
            self.back_function: str = self.back_code.co_name
            self.back_globals = back.f_globals
            self.back_locals = back.f_locals

            self.back_package: str = self.back_globals.get('__package__', None)
            self.back_globals_name: str = self.back_globals.get('__name__', None)
            if (file := self.back_globals.get('__file__', None)) is not None:
                self.back_file: Path = Path(file).resolved
                self.back_parent: Path = self.back_file.parent
                self.back_file_module: str = inspect.getmodulename(self.back_file.text)

            self.back_locals_name: str = self.back_locals.get('__name__', None)

        if back_f_back := getattr(back, 'f_back', None):
            if 'importlib._bootstrap' in str(back_f_back):
                if frame_back_back := getattr(back_f_back, 'f_back', None) is not None:
                    back = frame_back_back
            self.back_back = getattr(back, 'f_back', None)

            self.back_back_code: CodeType = back_f_back.f_code
            self.back_back_lineno: CodeType = back_f_back.f_lineno
            self.back_back_function: str = self.back_back_code.co_name
            self.back_back_globals = back_f_back.f_globals
            self.back_back_locals = back_f_back.f_locals

            self.back_back_package: str = self.back_back_globals.get('__package__', None)
            self.back_back_globals_name: str = self.back_back_globals.get('__name__', None)
            if (file := self.back_back_globals.get('__file__', None)) is not None:
                self.back_back_file: Path = Path(file).resolved
                self.back_back_parent: Path = self.back_back_file.parent
                self.back_back_file_module: str = inspect.getmodulename(self.back_back_file.text)

            self.back_back_locals_name: str = self.back_back_locals.get('__name__', None)

    @classmethod
    def func(cls, back: bool = False) -> Any:
        return cls().back_back_function if back else cls().back_function

    @classmethod
    def func_line(cls):
        f = cls()
        return f.back_function, f.back_lineno

    def installed(self, p: Any = None, index: int = index, ctx: int = ctx) -> bool:
        """
        Checks if path installed in sys.

        Args:
            p: path
            index: index
            ctx: context

        Returns:
            bool:
        """
        p = str(p) if p else str(self.__class__(index, ctx).back_file)
        return True if p.startswith(str(Py.exe_prefix)) or p.startswith(str(Py.sys_prefix)) else False

    @classmethod
    def vars_all(cls) -> list:
        return [
            key for key, value in cls().back_globals.items() if key[:1] != '_' and (
                    isinstance(value, str) or
                    isinstance(value, int) or
                    isinstance(value, list) or
                    isinstance(value, tuple) or
                    isinstance(value, set) or
                    isinstance(value, float) or
                    isinstance(value, dict) or
                    isinstance(value, Path) or
                    isinstance(value, Url)
            )
        ]


# </editor-fold>

# <editor-fold desc="LogR">
_level_file_default = LogLevel.DEBUG.value
_level_stream_default = LogLevel.ERROR.value


class LogR(verboselogs.VerboseLogger):
    file: int = _level_file_default
    stream: int = _level_stream_default
    packages: int = _level_stream_default
    all: dict = dict(package={}, packages={}, handlers=set(), root=set())
    manager: Optional[Logger] = None
    package: str = None
    format = dict(fh='large', rh='large')
    formats = dict(
        fh=dict(
            short='%(thin)s%(white)s[ %(log_color)s%(levelname)-8s%(white)s ] [ %(log_color)s%(name)-30s%(white)s ] '
                  '%(white)s %(log_color)s%(message)s %(white)s%(reset)s',
            large_func='%(thin)s%(white)s[%(log_color)s%(asctime)s%(white)s] %(white)s[%(log_color)s%(levelname)s%('
                       'white)s] '
                       '%(white)s[%(log_color)s%(name)s%(white)s] '
                       '%(white)s[%(log_color)s%(funcName)s%(white)s:%(log_color)s%(lineno)d%(white)s] '
                       '%(log_color)s%(message)s%(white)s%(reset)s',
            large='%(thin)s%(white)s[%(log_color)s%(asctime)s%(white)s] %(white)s[%(log_color)s%(levelname)s%(white)s] '
                  '%(white)s[%(log_color)s%(name)s%(white)s] '
                  '%(log_color)s%(message)s%(white)s%(reset)s',
            large_thread='%(thin)s%(white)s[%(log_color)s%(asctime)s%(white)s] %(white)s[%(log_color)s%(levelname)s%('
                         'white)s] '
                         '%(white)s[%(log_color)s%(name)s%(white)s] '
                         '%(white)s[%(log_color)s%(funcName)s%(white)s:%(log_color)s%(lineno)d%(white)s] '
                         '%(white)s[%(log_color)s%(threadName)s%(white)s] '
                         '%(log_color)s%(message)s%(white)s%(reset)s',
            date='%(thin)s%(white)s[%(log_color)s%(asctime)s%(reset)s%(white)s] '
                 '%(white)s[%(log_color)s%(levelname)s%(white)s] %(white)s[%(log_color)s%(name)s%(white)s] '
                 '%(white)s[%(log_color)s%(filename)s%(reset)s:%(log_color)s%(lineno)d%(reset)s - '
                 '%(log_color)s%(module)s%(reset)s - %(log_color)s%(funcName)s%(reset)s%(white)s] '
                 '%(white)s %(log_color)s%(message)s %(white)s%(reset)s'),
        rh=dict(
            short='%(message)s',
            large='[%(name)s| %(module)s | %(funcName)s %(lineno)s] - %(message)s',
            large_thread='[%(name)s| %(module)s| %(threadName)s | %(funcName)s %(lineno)s] - %(message)s'))
    colors: tuple = ('white', 'cyan', 'green', 'yellow', 'purple', 'blue', 'red', 'fg_bold_red',)
    rotate: dict = dict(count=5, interval=1, when='d')
    propagate: bool = True
    mode: str = 'a'
    path: Any = None

    __exclude_class_asdict__ = True

    def __init__(self, name: str = None, level: Union[str, int] = packages):
        self.name = name
        self.level = self._get_level(level)
        super().__init__(self.name, self.level)

    @property
    def child(self) -> LogR:
        """
        Child logger with module name.

        Returns:
            child logger
        """
        frame = Frame()
        name = frame.back_file_module
        # name = frame.back_parent.name if (module := frame.back_file_module) == '__init__' else \
        #     f'{frame.back_parent.name}.{module}'
        _l = self.getChild(name)
        _l.level_set()
        return _l

    @classmethod
    def get_log(cls, name: str = None, p: Union[PathLike, Pathlib, Path] = None, file: Union[str, int] = file,
                stream: Union[str, int] = stream, packages: Union[str, int] = packages, installed: bool = True,
                markup: bool = True) -> Union[LogR, Logger]:
        """
        Sets Logger.

        Args:
            name: name
            p: path
            file: file
            stream: stream
            packages: packages
            installed: installed
            markup: markup

        Returns:
            Union[LogR, Logger]:
        """
        f = Frame()
        cls.path = p
        cls.file = file
        cls.stream = stream
        cls.packages = packages
        logging.setLoggerClass(LogR)
        logger = logging.getLogger(name if name else f.back_parent.name)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.propagate = cls.propagate
        logger.package = logger.name
        if root := (getattr(logger, 'parent', None)):
            root.setLevel(cls._get_level(cls.packages))
        logger.setLevel(cls._get_min(cls.file, cls.stream))

        if installed or cls.mode == 'a':
            fh = logging.handlers.TimedRotatingFileHandler(
                str(cls.path), when=cls.rotate['when'], interval=cls.rotate['interval'],
                backupCount=cls.rotate['count'])
        else:
            fh = logging.FileHandler(p.text, cls.mode)
        fh_formatter = colorlog.ColoredFormatter(fmt=cls.formats['fh'][cls.format['fh']],
                                                 log_colors=dict(zip(LogLevel.attrs(), cls.colors)))
        fh.setLevel(cls.file)
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

        rh_formatter = logging.Formatter(fmt=cls.formats['rh'][cls.format['rh']])
        rh = rich.logging.RichHandler(markup=markup)
        rh.setLevel(cls.stream)
        rh.setFormatter(rh_formatter)
        logger.addHandler(rh)

        cls.manager = getattr(logger, 'manager', None)
        cls.level_set('packages', cls._get_level(cls.packages))
        return logger

    @classmethod
    def _get_level(cls, level: Union[str, int]) -> int:
        """
        Get Level Value

        Args:
            level: level

        Returns:
            int:
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        return level

    @classmethod
    def _get_min(cls, x: Union[str, int], y: Union[str, int]) -> int:
        """
        Get Min Value

        Args:
            x: x
            y: y

        Returns:
            int:
        """
        return min(cls._get_level(x), cls._get_level(y))

    @classmethod
    def level_set(cls, attr: str = None, value: Union[str, int] = None):
        """
        Helper to sets Handler or Logger Level for caller setter.

        Args:
            attr: handler or logger attribute.
            value: level value to set.
        """
        if attr is not None:
            value = getattr(cls, attr) if value is None else cls._get_level(value)
            setattr(cls, attr, value)

        cls._level_set_logger('root', cls.packages)
        if (loggerDict := getattr(cls.manager, 'loggerDict', None)) is not None:
            for name in loggerDict:
                key = 'package' if name.startswith(cls.package if cls.package else name) else 'packages'
                level = cls._get_min(cls.file, cls.stream) if key == 'package' else cls.packages
                cls._level_set_logger(name, level, key)

    @classmethod
    def _level_set_handler(cls, logger):
        """
        Sets Handler Level.

        Args:
            logger: logger
        """
        if logger.hasHandlers():
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.TimedRotatingFileHandler) \
                        or isinstance(handler, logging.FileHandler):
                    handler.setLevel(cls._get_level(cls.file))
                if isinstance(handler, logging.StreamHandler) \
                        and not isinstance(handler, logging.handlers.TimedRotatingFileHandler) \
                        and not isinstance(handler, logging.FileHandler):
                    handler.setLevel(cls._get_level(cls.stream))
                key = logger.name if logger.name == 'root' else 'handlers'
                cls.all[key].add(handler)

    @classmethod
    def _level_set_logger(cls, name: str, level: Union[str, int], key: str = None):
        """
        Sets Logger Level.

        Args:
            name: logger name.
            level: level value.
            key: `LogR.all` key.
        """
        logger = logging.getLogger(name)
        logger.setLevel(cls._get_level(level))
        if key is None:
            cls.all[name].add(logger)
        else:
            cls.all[key][name] = logger
        if name == cls.package:
            cls._level_set_handler(logger)

    def out(self, msg: str, err: ExitCode = None, exc: Any = None):
        """
        Prints message, logs and raise exception if enabled.

        Args:
            msg: if only message is provided: logs msg if enabled and prints green msg.
            err: if err is provided: logs msg if enabled, prints red msg and `sys.exit` with `err.value`.
            exc: if exception is provided, err must be provided and logs critical with exception.

        Raises:
            AttributeError: AttributeError
        """
        if exc is not None and err is None:
            raise AttributeError(f'ExitCode must be provided when exception is not None: {err}')
        if exc is not None:
            try:
                raise exc(msg)
            except exc as e:
                self.critical(e)
                red(f'[{err.name}]: {msg}')
                sys.exit(err.value)
        elif exc is None and err is None:
            self.debug(msg)
            green(msg)
        else:
            self.debug(msg)
            red(f'[{err.name}]: {msg}')
            sys.exit(err.value)

    @classmethod
    def prepare_msg(cls, msg, *args) -> str:
        try:
            frame_2 = inspect.stack()[2]
            frame_3 = inspect.stack()[3]
            frame = frame_2
            if 'asyncio' in frame_2.filename:
                frame = frame_3
            if 'asyncio' in frame_3.filename:
                frame = frame_2
            frame_path = Path(frame.filename)
            add = f'({frame_path.parent.name}/{frame_path.name} | {frame.function}: {frame.lineno}) '
        except IndexError:
            add = str()
        rv = ', '.join(str(item) for item in (msg, *args,))
        rv = add + rv if add else rv
        return rv

    def log(self, level, msg, *args, **kwargs):
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            self._log(level, self.prepare_msg(msg, *args), (), **kwargs)

    async def aspam(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SPAM):
            await executor(self._log, verboselogs.SPAM, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def adebug(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            await executor(self._log, logging.DEBUG, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def averbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.VERBOSE):
            await executor(self._log, verboselogs.VERBOSE, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def ainfo(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            await executor(self._log, logging.INFO, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def anotice(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.NOTICE):
            await executor(self._log, verboselogs.NOTICE, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def awarning(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            await executor(self._log, logging.WARNING, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def asuccess(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SUCCESS):
            await executor(self._log, verboselogs.SUCCESS, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def aerror(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            await executor(self._log, logging.ERROR, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def acritical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            await executor(self._log, logging.CRITICAL, self.prepare_msg(msg, *args), (),
                           pool=Executor.THREAD, **kwargs)

    async def aexception(self, msg, *args, exc_info=True, **kwargs):
        await self.aerror(self.prepare_msg(True, msg, *args), (), exc_info=exc_info,
                          pool=Executor.THREAD, **kwargs)

    def spam(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SPAM):
            self._log(verboselogs.SPAM, self.prepare_msg(msg, *args), (), **kwargs)

    def debug(self, msg, *args, **kwargs):  # Start, End
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, self.prepare_msg(msg, *args), (), **kwargs)

    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.VERBOSE):
            self._log(verboselogs.VERBOSE, self.prepare_msg(msg, *args), (), **kwargs)

    def info(self, msg, *args, **kwargs):  # Released
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, self.prepare_msg(msg, *args), (), **kwargs)

    def notice(self, msg, *args, **kwargs):  # Acquired
        if self.isEnabledFor(verboselogs.NOTICE):
            self._log(verboselogs.NOTICE, self.prepare_msg(msg, *args), (), **kwargs)

    def warning(self, msg, *args, **kwargs):  # Waiting
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, self.prepare_msg(msg, *args), (), **kwargs)

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SUCCESS):
            self._log(verboselogs.SUCCESS, self.prepare_msg(msg, *args), (), **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, self.prepare_msg(msg, *args), (), **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, self.prepare_msg(msg, *args), (), **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.error(self.prepare_msg(False, msg, *args), (), exc_info=exc_info, **kwargs)


UnionStrLogger = Union[str, Logger, LogR]


# </editor-fold>

# <editor-fold desc="Env">
@dataclasses.dataclass
class Env(AsDict):
    """
    Env Class.

    # Examples:
        # >>> import os
        # >>> from bapy import Path, m
        # >>>
        # >>> # Cleaning
        # >>> project_env_file = m.project.path.joinpath('.env')
        # >>> project_env_file.rm()
        # >>> tmp_path = Path('/tmp')
        # >>> tmp_env_file = tmp_path.joinpath('.env')
        # >>> tmp_env_file.rm()
        # >>>
        # >>> # env.environ tests
        # >>> env = Env()
        # >>> env.environ = dict(a=1, b=2)
        # >>> env.environ
        # {'a': '1', 'b': '2'}
        # >>> os.environ['A']
        # '1'
        # >>> os.environ['B']
        # '2'
        # >>> env.asdict  # doctest: +ELLIPSIS
        # {'_environ': ['a', 'b'], 'environ': {'a': '1', 'b': '2'}, ...
        # >>>
        # >>> # env._Env tests
        # >>> tmp_path = Path().cd('/tmp')
        # >>> tmp_env_file = tmp_path.joinpath('.env')
        # >>> tmp_env_file.write_text('export LOG_LEVEL=DEBUG')
        # 22
        # >>> assert tmp_env_file.read_text() == 'export LOG_LEVEL=DEBUG'
        # >>> env = Env()
        # >>> assert env._Env.log_level('LOG_LEVEL') == 10
        # >>> assert env._Env.dump()['LOG_LEVEL']  == 10
        # >>> tmp_env_file.rm()
    """
    prefix: str = _path_installed.prefix
    _environ: set = None
    _Env = None
    file: Path = datafield(default=None, init=False)
    Env = collections.namedtuple('Env', 'default value')
    Field = collections.namedtuple('Field', 'default prefix type')

    bapy: Union[Env, Field] = datafield(default=None, init=False)
    debug: Union[Env, Field, bool] = datafield(default=False, init=False)
    debug_async: Union[Env, Field, bool] = datafield(default=debug.default, init=False)
    ic: Union[Env, Field, bool] = datafield(default=debug.default, init=False)
    log_level: Union[Env, Field] = datafield(default=None, init=False)
    log_level_file: Union[Env, Field] = datafield(default=None, init=False)
    pen: Union[Env, Field] = datafield(default=None, init=False)
    username: Union[Env, Field] = datafield(default=None, init=False)
    verbose: Union[Env, Field, bool] = datafield(default=debug.default, init=False)

    sem_default = dict(MAX=2000, MONGO=499, NMAP=500, OS=300, SSH=500, PING=750, SOCKET=400)
    sem = dict()
    sems: dict = datafield(default_factory=dict, init=False)

    # TODO: comprobar que no hace deepcopy.

    # __asdict_exclude__ = [_Env, ]

    def __post_init__(self):
        if self._Env is None:
            self._Env = environs.Env()

        self.file = Path.cwd().find_up()
        if self.file:
            dotenv.load_dotenv(self.file.text, verbose=True, override=True)

        self.Var = collections.namedtuple('Var', 'bapy debug debug_async ic log_level log_level_file '
                                                 'username pen verbose ')
        self.var = self.Var(*self.Var._fields)

        self.bapy = self.nferx_atlas_password = self.pen = self.username = self.Field(None, None, None)

        self.debug = self.debug_async = self.ic = self.verbose = self.Field(Env.debug, True, 'bool')
        self.log_level = self.Field(_level_stream_default, True, 'log_level')
        self.log_level_file = self.Field(_level_file_default, True, 'log_level')

        for item in self.Var._fields:
            field = getattr(self, item)
            function = getattr(self._Env, field.type) if field.type else self._Env
            name = getattr(self.var, item).upper()
            var = (upper_prefix(name, prefix=self.prefix), field.default) \
                if field.prefix else (name, os.environ.get(name, field.default))
            value = function(*var)
            setattr(self, item, self.Env(field.default,
                                         (Path(value) if value else User.home) if item in ['bapy', 'pen'] else value))

        self.sem = {name: {
            Priority.LOW: asyncio.Semaphore(
                val if (val := round(
                    self._Env.int(upper_prefix(name, prefix=self.prefix), default) / Priority.LOW.value)) else 1)
        } for name, default in self.sem_default.items()}
        for name in self.sem:
            self.sem[name][Priority.HIGH] = asyncio.Semaphore(
                val if (val := round(self.sem[name][Priority.LOW]._value / Priority.HIGH.value)) else 1)

        self.sems = {name: {
            priority.name: dict(default=int(round(self.sem_default[name] / (
                Priority.LOW.value if priority is Priority.LOW else Priority.HIGH.value
            ))), value=s._value) for priority, s in priority_dict.items()
        } for name, priority_dict in self.sem.items()}

        if self.log_level.value == 'DEBUG' or self.log_level.value == logging.DEBUG:
            self.verbose = self.Env(self.verbose.default, True)
        if self.verbose.value:
            self.log_level = self.Env(self.log_level.default, logging.DEBUG)
        self.aiodebug()

    def aiodebug(self, enable: bool = False):
        def ok():
            tracemalloc.start()
            self.environ = {'PYTHONASYNCIODEBUG': 1}
            logger = logging.getLogger('asyncio')
            logger.setLevel(LogLevel.DEBUG.value)
            warnings.simplefilter("always", ResourceWarning)

        def no():
            tracemalloc.stop()
            self.environ = {'PYTHONASYNCIODEBUG': 0}
            logger = logging.getLogger('asyncio')
            logger.setLevel(LogLevel.ERROR.value)
            warnings.simplefilter("ignore", ResourceWarning)

        if self.debug_async.value or enable:
            return ok()
        return no()

    @property
    def environ(self) -> dict:
        """
        OS Environ Vars Set.

        Returns:
            dict:
        """
        if self._environ:
            return {item: os.environ.get(item.upper()) for item in self._environ}

    @environ.setter
    def environ(self, value: dict):
        """
        Sets `os.environ` Vars and stores keys in `self.environ`.

        Args:
            value: value
        """
        if not self.environ:
            self._environ = set()
        for key in value:
            os.environ[key.upper()] = str(value[key])
            self._environ.add(key)


# </editor-fold>


_env = Env()
_log = LogR.get_log(name=_path_installed.name, p=_path_installed.log_file, file=_env.log_level_file.value,
                    stream=_env.log_level.value, installed=_path_installed.installed)


# <editor-fold desc="Count">
@dataclasses.dataclass
class Count:
    percentage: str = str()
    ok: int = int()
    error: int = int()
    no: int = int()
    count: int = int()
    total: int = 1
    verbose: bool = False
    log: LogR = _log

    async def aouterr(self, msg: str = str()):
        await executor(self.outerr, msg)

    async def aoutno(self, msg: str = str()):
        await executor(self.outno, msg)

    async def aoutok(self, msg: str = str()):
        await executor(self.outok, msg)

    def console(self, msg, error: bool = False, no: bool = False):
        percentage = self.percentage
        ok = self.ok
        total = self.total

        if self.verbose:
            if error:
                cprint(f"[bold blue]{self.percentage}[white] "
                       f"\\[ok: [bold green]{self.ok}[white], "
                       f"error: [bold red]{self.error}[white], "
                       f"no: [bold magenta]{self.no}[white], "
                       f"total: [bold blue]{self.total}[white]] "
                       f"[bold red]{msg}")
                self.log.error(self.format(msg))
                return
            if no:
                cprint(f"[bold blue]{self.percentage}[white] "
                       f"\\[ok: [bold green]{self.ok}[white], "
                       f"error: [bold red]{self.error}[white], "
                       f"no: [bold magenta]{self.no}[white], "
                       f"total: [bold blue]{self.total}[white]] "
                       f"[bold magenta]{msg}")

            cprint(f"[bold green]{msg}[white] "
                   f"\\[ok: [bold green]{ok}[white], "
                   f"error: [bold red]{self.error}[white], "
                   f"no: [bold magenta]{self.no}[white], "
                   f"total: [bold blue]{total}[white]] "
                   f"[bold blue]{percentage}[white] ")
        self.log.debug(msg, f'{ok=}', f'{total=}', f'{percentage=}')

    def format(self, msg):
        try:
            return fm(self, msg)
        except IndexError:
            self.log.debug('fm IndexError')

    def get_percentage(self):
        return f'{round(self.count * 100 / self.total, 2)}%'

    def outerr(self, msg: str = str()):
        self.error += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg, error=True)

    def outno(self, msg: str = str()):
        self.no += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg, no=True)

    def outok(self, msg: str = str()):
        self.ok += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg)


# </editor-fold>

# <editor-fold desc="Kill">
@dataclasses.dataclass
class Kill:
    """Exit class"""
    signal: str = '9'
    cmd: str = datafield(default='sudo kill', init=False)
    command: str = _path_installed.name
    count_values: tuple = ('nmap', 'ping', 'ssh',)
    log: LogR = _log
    parameter: str = str()
    current_process = None
    current_pid: int = datafield(default=int(), init=False)
    exception: sys.exc_info = datafield(default=None, init=False)
    exception_thread: str = datafield(default=str(), init=False)

    def __post_init__(self):
        self.cmd = f'{self.cmd} -{self.signal}'
        self.current_pid = os.getpid()
        self.current_process = psutil.Process(self.current_pid)

    @staticmethod
    def count(text: str = count_values[0]) -> int:
        out_cmd = cmd(Kill.count_cmd(text=text))
        return len(out_cmd.stdout) if out_cmd.stdout else 0

    @staticmethod
    async def count_async(text: str = count_values[0]) -> int:
        out_cmd = await aiocmd(Kill.count_cmd(text=text), utf8=True, lines=True)
        return len(out_cmd.stdout) if out_cmd.stdout else 0

    @staticmethod
    def count_cmd(text: str = count_values[0]) -> str:
        return f'pgrep -a -c {shlex.quote(text)}'

    def exit(self):
        function = inspect.currentframe().f_code.co_name
        if self.log:
            self.log.spam(f'{function=}', f'{self.current_pid=}')
        try:
            for child in self.current_process.children(recursive=True):
                child.kill()
                cmd(f'{self.cmd} {child.pid}')
                if self.log:
                    self.log.spam('Killed current child', f'{function=}', f'{self.current_pid=}', f'{child.pid=}')
        except psutil.AccessDenied as exception:
            if self.log:
                self.log.spam('Kill current child', f'{function=}', f'{self.current_pid=}', f'{exception=}')
        except psutil.NoSuchProcess as exception:
            if self.log:
                self.log.spam('Killed current child sudo', f'{function=}', f'{self.current_pid=}', f'{exception=}')

    def stat(self, verbose: bool = True):
        stat = {item: int() for item in ['children', ''] if item}
        stat['threads'] = self.current_process.threads()
        stat['memory_percent'] = self.current_process.memory_percent()
        stat['cpu_percent'] = self.current_process.cpu_percent()

        if verbose and self.log:
            self.log.debug('Process', f'{stat=}')
        return stat

    def stop(self, command: str = None, parameter: str = None):
        function = inspect.currentframe().f_code.co_name
        self.command = command if command else self.command
        self.parameter = parameter if parameter else self.parameter
        if self.log:
            text = f'{function=}', f'{self.current_pid=}', f'{self.command=}'
            if self.command:
                self.log.debug(text)
            else:
                self.log.error(text)
                return
        attrs = ['pid', 'cmdline', 'username']
        for process in psutil.process_iter(attrs):
            if isinstance(process.info['cmdline'], list):
                if len(process.info['cmdline']) > 1:
                    if (self.command in process.info['cmdline'][0] or self.command in process.info['cmdline'][1]) \
                            and self.parameter in process.info['cmdline'][1:]:
                        if self.log:
                            self.log.spam(f'{function=}', f'{process.info=}')
                        if self.parameter in process.info['cmdline']:
                            if self.log:
                                self.log.spam(f'{function=}', f'{self.parameter=}', f'{process.info["cmdline"]=}')
                            try:
                                for p in process.children(recursive=True):
                                    p.kill()
                                    cmd(f'{self.cmd} {p.pid}')
                                    if self.log:
                                        self.log.spam('Killed child', f'{function=}', f'{p.pid=}')
                            except psutil.AccessDenied as exception:
                                if self.log:
                                    self.log.spam('Kill child', f'{function=}', f'{exception=}')
                            except psutil.NoSuchProcess as exception:
                                if self.log:
                                    self.log.spam(exception)
                            try:
                                if self.current_pid != process.pid:
                                    process.kill()
                                    if self.log:
                                        self.log.spam('Killed other', f'{function=}', f'{process.pid=}',
                                                      f'{self.current_pid=}')
                            except psutil.AccessDenied as exception:
                                if self.log:
                                    self.log.spam('Kill other', f'{function=}', f'{process.pid=}',
                                                  f'{self.current_pid=}', f'{exception=}')
                                cmd(f'{self.cmd} {process.pid}')
                                if self.log:
                                    self.log.spam('Killed other sudo', f'{function=}', f'{process.pid=}',
                                                  f'{self.current_pid=}')
                            except psutil.NoSuchProcess as exception:
                                if self.log:
                                    self.log.spam(exception)


# </editor-fold>

# <editor-fold desc="GitHub">
@dataclasses.dataclass
class GitHub:
    path: Optional[Path] = _path_installed.project \
        if _path_installed.project and not _path_installed.installed else None
    clone_rm: bool = None
    config_path: Any = None
    id_rsa: Any = None
    log: Any = _log
    username: str = None
    _version_new: str = None
    _version_old: str = None
    cli: dict[str, list] = datafield(default_factory=dict, init=False)
    cmd: Optional[git.Repo.GitCommandWrapperType] = datafield(default=None, init=False)
    config: git.GitConfigParser = datafield(default=None, init=False)
    remote = None
    remote_urls: list = datafield(default_factory=list, init=False)
    repo: git.Repo = datafield(default=None, init=False)
    repo_dirs: box.Box = datafield(default_factory=box.Box, init=False)
    git: git.Git = datafield(default=None, init=False)
    url: Url = datafield(default=None, init=False)

    def __post_init__(self):
        if self.path:
            self.init_clone()
            self.repo_dirs = self.path.scan(option=PathOption.DIRS)
        self.cli = {
            'test_usable': ['git', 'rev-parse', '--git-dir'],
            'commit': ['git', 'commit', '-F'],
        }
        self.config_path = self.config_path if self.config_path else User.git_config_path
        self.config = git.GitConfigParser(self.config_path)
        self.id_rsa = self.id_rsa if self.id_rsa else User.id_rsa
        self.username = self.username if self.username else self.config.get_value(section='user', option='username',
                                                                                  default=str())
        os.environ['GIT_SSH_COMMAND'] = f'ssh -i {self.id_rsa} -o UserKnownHostsFile=/dev/null ' \
                                        f'-o StrictHostKeyChecking=no -o IdentitiesOnly=yes'

    def add(self, force: bool = False, write: bool = True):
        """
        Adds untracked files to Git.

        Args:
            force: force
            write: write
        """
        rv = list()
        if hasattr(self.repo, 'untracked_files'):
            for file in self.repo.untracked_files:
                added = self.repo.index.add(file, force=force, write=write)
                rv.append(added[0][3])
        if self.log:
            self.log.spam(rv)
        return rv

    @staticmethod
    def add_path(p):
        return subprocess.check_output(['git', 'add', '--update', p])

    @staticmethod
    def assert_nondirty():
        lines = [
            line.strip()
            for line in subprocess.check_output(
                ['git', 'status', '--porcelain']
            ).splitlines()
            if not line.strip().startswith(b"??")
        ]

        if lines:
            raise BapyGitDirectoryIsDirty(
                "Git working directory is not clean:\n{}".format(
                    b"\n".join(lines).decode()
                )
            )

    def clone(self, url: str = None, p: Path = None, rm: bool = clone_rm):
        """
        Wrapper for :meth:`git.Repo.clone_from`.
        #
        # Examples:
        #     >>> from bapy import Path, m
        #     >>> ssh_options = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o IdentitiesOnly=yes'
        #     >>> os.environ['GIT_SSH_COMMAND'] = f'ssh -i {User.id_rsa} {ssh_options}'
        #     >>> repo = m.project.name
        #     >>> dest_dir = Path(f'/tmp/{repo}')
        #     >>> dest_dir.rm()
        #     >>> GitHub.clone(Url.lumenbiomics(http=False, repo=repo), dest_dir) #doctest: +ELLIPSIS
        #     <git.repo.base.Repo '/tmp/bapy/.git'>
        #     >>> dest_dir.rm()

        Args:
            url: git url
            p: destination path
            rm: remove before clone

        Returns:
            git.Repo:
        """
        self.clone_rm = rm if rm else self.clone_rm
        if self.clone_rm:
            self.path.rm()
        rv = git.Repo.clone_from(url=url if url else self.url, to_path=p.text if p else self.path.text)
        self.repo_dirs = self.path.scan(option=PathOption.DIRS)
        if self.log:
            self.log.spam(rv)
        return rv

    def commit_cmd(self, message: str = None) -> None:
        if message is None:
            message = self.message
        commit = self.cmd.commit('-a', '-m', message)
        if self.log:
            self.log.spam(commit)
        return commit

    def commit_cli(self, message, ctx, extra_args=None):
        extra_args = extra_args or []
        with tempfile.NamedTemporaryFile('wb', delete=False) as f:
            f.write(message.encode('utf-8'))
        env = os.environ.copy()
        env['HGENCODING'] = 'utf-8'
        for key in ('current_version', 'new_version'):
            env[str('BUMPVERSION_' + key.upper())] = str(ctx[key])
        try:
            subprocess.check_output(
                self.cli['commit'] + [f.name] + extra_args, env=env
            )
        except subprocess.CalledProcessError as exc:
            err_msg = f'Failed to run {exc.cmd}: return code {exc.returncode}, output: {exc.output}'
            if self.log:
                self.log.spam(err_msg)
            raise exc
        finally:
            os.unlink(f.name)

    def fetch(self):
        rv = self.remote.fetch()
        self.repo_dirs = self.path.scan(option=PathOption.DIRS)
        if self.log:
            self.log.spam(rv)
        return rv

    def init_clone(self):
        self.url = Url.lumenbiomics(repo=self.path.name)

        try:
            self.repo = git.Repo(self.path)
        except git.exc.NoSuchPathError:
            self.repo = self.clone()
        except git.exc.InvalidGitRepositoryError as exception:
            if self.log:
                self.log.error(exception)

        if self.path.exists() is False:
            self.repo = self.clone()

        if self.repo:
            self.cmd = self.repo.git
            self.remote = self.repo.remote()
            self.remote_urls = [url for url in self.remote.urls]
            self.version_old = self.repo.tags
            self.repo_dirs = self.path.scan(option=PathOption.DIRS)

    def is_usable(self):
        try:
            return (
                    subprocess.call(
                        self.cli['test_usable'],
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                    )
                    == 0
            )
        except OSError as e:
            if e.errno in (errno.ENOENT, errno.EACCES):
                return False
            raise

    @staticmethod
    def latest_tag_info():
        try:
            subprocess.check_output(['git', 'update-index', '--refresh'])

            describe_out = (
                subprocess.check_output(
                    [
                        'git',
                        'describe',
                        '--dirty',
                        '--tags',
                        '--long',
                        '--abbrev=40',
                        '--match=v*',
                    ],
                    stderr=subprocess.STDOUT,
                ).decode().split("-")
            )
        except subprocess.CalledProcessError:
            return {}

        inf = {}

        if describe_out[-1].strip() == 'dirty':
            inf['dirty'] = True
            describe_out.pop()

        inf['commit_sha'] = describe_out.pop().lstrip('g')
        inf['distance_to_latest_tag'] = int(describe_out.pop())
        inf['current_version'] = '-'.join(describe_out).lstrip('v')

        return inf

    @property
    def message(self):
        return f'Bump: {self.version_old} --> {self.version_new}'

    def pull(self):
        rv = self.remote.pull()
        self.repo_dirs = self.path.scan(option=PathOption.DIRS)
        if self.log:
            self.log.spam(rv)
        return rv

    def push(self, remote: str = 'origin'):
        rv = self.repo.remote(remote).push()
        if self.log:
            self.log.spam(f'{rv[0].summary=}', f'{rv[0].flags=}')
        return rv[0].summary, rv[0].flags

    @property
    def status(self):
        rv = self.cmd.status('--porcelain')
        if self.log:
            self.log.spam(rv)
        return rv

    def tag(self, v: str = None):
        if v is None:
            v = self.version_new
        rv = self.repo.create_tag(v)
        if self.log:
            self.log.spam(rv)
        return rv

    @staticmethod
    def tag_cli(sign, tag, message):
        command = ['git', 'tag', tag]
        if sign:
            command += ['--sign']
        if message:
            command += ['--message', message]
        return subprocess.check_output(command)

    @property
    def version_new(self):
        return self._version_new

    @version_new.setter
    def version_new(self, v: str):
        self._version_new = v

    @property
    def version_old(self):
        return self._version_old

    @version_old.setter
    def version_old(self, v: str):
        self._version_old = v


# </editor-fold>

# <editor-fold desc="Ip">
@dataclasses.dataclass
class Ip(AsDict):
    """
    IP Class.

    Examples:
        >>> assert asyncio.run(Ip(ip='10:12:14').init) is None
        >>> valid = asyncio.run(Ip(ip='8.8.8.8').init)
        >>> assert valid.info['ipv4'] == '8.8.8.8'
        >>> assert valid.info['ipv6'] is False
        >>> assert valid.location['country_name'] == 'United States'
        >>> assert valid.location['city'] is None
        >>> assert valid.ping is True
        >>> assert 'ping' in valid.attrs()
        >>> assert valid.asdict['info']['global'] is True
        >>> local = asyncio.run(Ip(ip='192.168.1.134').init)
        >>> assert local.ping is False
        >>> myip = asyncio.run(Ip().init)
        >>> assert myip.info['global'] is True
    """
    info: dict = datafield(default_factory=dict, init=False)
    _ip: Optional[IPvType] = None
    location: dict = datafield(default_factory=dict, init=False)
    log = _log
    name: str = None
    retry = 0
    retry_max = 3
    retry_sleep = 10

    def __post_init__(self):
        if self.ip is None:
            self.ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    @property
    async def init(self) -> Optional[Ip]:
        """
        Ip Instance.

        Returns:
            Optional[Ip]:
        """
        if await self.IPClass:
            _ = await self.Location
            try:
                self.name = socket.getfqdn(self.ip)
            except socket.herror:
                pass
            return self

    @property
    def ip(self) -> Optional[IPvType]:
        if self._ip is None:
            self._ip = ipaddr(urllib.request.urlopen('https://ident.me').read().decode('utf8'))
        return self._ip

    @ip.setter
    def ip(self, value: Optional[IPAddressLike]):
        if value:
            self._ip = ipaddr(value)
        else:
            self._ip = value

    @property
    async def IPClass(self) -> Optional[IPvType]:
        """
        Validates, stores ip, ipv4 and ipv6 as str and returns IPvType.

        Returns:
            Optional[IPvType]:
        """
        try:
            rv = await sync_to_async(ipaddr)(self.ip)
            self.ip = rv.compressed
            self.info['ipv4'] = rv.compressed if rv.version == 4 else False
            self.info['ipv6'] = rv.compressed if rv.version == 6 else False
            self.info['global'] = rv.is_global
            self.info['reverse_pointer'] = rv.reverse_pointer
            self.info['version'] = rv.version
        except ValueError:
            self.ip = rv = None
        return rv

    @property
    async def Location(self) -> Optional[dict]:
        """
        IP Location Info.

        Returns:
            Optional[dict]:
        """
        if self.ip:
            try:
                with await sync_to_async(urllib.request.urlopen)(
                        f'https://geolocation-db.com/json/697de680-a737-11ea-9820-af05f4014d91/{self.ip}') \
                        as geolocation:
                    location = await sync_to_async(json.loads)(geolocation.read().decode())
                self.location['city'] = location['city'] if location['city'] != 'Not found' else None
                self.location['country_code'] = location['country_code'] \
                    if location['country_code'] != 'Not found' else None
                self.location['country_name'] = location['country_name'] \
                    if location['country_name'] != 'Not found' else None
                self.location['latitude'] = location['latitude'] if location['latitude'] != 'Not found' else None
                self.location['longitude'] = location['longitude'] if location['longitude'] != 'Not found' else None
                self.location['postal'] = location['postal'] if location['postal'] != 'Not found' else None
                self.location['state'] = location['state'] if location['state'] != 'Not found' else None
                return location
            except urllib.error.HTTPError as exception:
                if self.retry < self.retry_max:
                    self.retry += 1
                    await asyncio.sleep(self.retry_sleep)
                    _ = await self.Location
                else:
                    self.log.error(f'{self.ip=}', f'{exception=}')


# </editor-fold>

# <editor-fold desc="Py">
@dataclasses.dataclass
class Py:
    """Python Server Information Class."""
    python_version: tuple[int] = platform.python_version_tuple()
    PY2: bool = True if int(python_version[0]) == 2 else False
    PY3: bool = True if int(python_version[0]) == 3 else False
    PY310: bool = True if PY3 and int(python_version[1]) == 10 else False
    PY39: bool = True if PY3 and int(python_version[1]) == 9 else False
    PY38: bool = True if PY3 and int(python_version[1]) == 8 else False
    PY37: bool = True if PY3 and int(python_version[1]) == 7 else False
    exe_path: Path = Path(sys.executable).resolved
    exe_name: str = exe_path.name
    sys_prefix: Path = Path(sys.base_prefix).resolved
    exe_prefix: Path = Path(sys.prefix).resolved
    sys_site: Path = sys_prefix / 'lib' / exe_name / 'site-packages'
    exe_site: Path = exe_prefix / 'lib' / exe_name / 'site-packages'
    VENV: bool = True if sys_prefix != exe_prefix else False
    exception: tuple = tuple()

    def __post_init__(self):
        if set(self.exception) == {True}:
            raise RuntimeError('Invalid python version', f'{self.python_version=}')


# </editor-fold>


Py(exception=(not Py.PY39, not Py.PY310))


# <editor-fold desc="Sem">
class SemEnum(EnumDict):

    def _generate_next_value_(self, start, count, last_values) -> dict[Priority, asyncio.Semaphore]:
        return _env.sem[self]

    async def text(self, *args, **kwargs) -> list:
        def _args():
            _vars = ['ip', ]
            return ', '.join([f'{_var}: {_val}' for _var in _vars if (_val := self.call.vars.loc.get(_var))])

        called = f'({self.call.file.parent.name}/{self.call.module} | {self.call.funcname}: {self.call.lineno} | ' \
                 f'{_args()}) '
        running = Kill.count() if self.name in Kill.count_values else str()
        prefix, kwargs = pop_default(kwargs, 'prefix')
        common = [f'{self.name=}', f'{self.priority.name=}', f'{self.call.task=}', f'{self.func.__qualname__=}',
                  f'{self.status=}',
                  f'{running=}', f'{called=}']
        suffix, kwargs = pop_default(kwargs, 'suffix')
        kw = [f'{key}: {value}' for key, value in kwargs.items()]
        return ([prefix] if prefix else list()) + common + list(args) + kw + ([suffix] if suffix else list())

    # noinspection PyAttributeOutsideInit
    async def sem(self, func: Callable, /, *args, priority: Priority = Priority.LOW,
                  exceptions: tuple = (KeyboardInterrupt,), nap: Nap = Nap.MONGO, **kwargs) -> Any:
        """
        Examples:
            >>> await Sem.OS.sem(executor, ipaddr, '8.8.8.8')
            >>> await Sem.MAX.sem(asyncio.to_thread, Sem.MAX.low)
        Args:
            func: func.
            priority: priority.
            exceptions: exceptions.
            nap: nap.
            **kwargs: **kwargs.

        Returns:
            Any:
        """
        self.call: Caller = caller()
        self.func: Union[Callable, property] = func
        self.priority: Priority = priority

        sem = self.value[Priority.LOW]
        using = Priority.LOW.name
        if priority == Priority.HIGH and self.value[Priority.LOW].locked():
            sem = self.value[priority]
            using = priority.name
        await _log.awarning(*await self.text(f'{using=}', suffix='Waiting'))
        async with sem:
            await _log.anotice(*await self.text(f'{using=}', suffix='Acquired'))
            while True:
                try:
                    if self.call.coro:
                        rv = await func(*args, **kwargs)
                    else:
                        rv = func(*args, **kwargs)
                    break
                except exceptions as exception:
                    await _log.aspam(*await self.text(prefix='Waiting for:', using=using, suffix=repr(exception)))
                    await nap.asleep()
                    continue
        await _log.ainfo(*await self.text(using=using, suffix='Released'))
        return rv

    @property
    def high(self) -> dict[str, int]:
        return self.value[Priority.HIGH]._value

    @property
    def low(self) -> dict[str, int]:
        return self.value[Priority.LOW]._value

    @property
    def status(self) -> dict[str, int]:
        return {priority.name: sem._value for priority, sem in self.value.items()}

    @property
    def total(self) -> dict[str, int]:
        return {priority.name: sem._value for priority, sem in _env.sem[self.name].items()}


class Sem(SemEnum):
    MAX = enum.auto()
    MONGO = enum.auto()
    NMAP = enum.auto()
    OS = enum.auto()
    SSH = enum.auto()
    PING = enum.auto()
    SOCKET = enum.auto()


# </editor-fold>

# <editor-fold desc="Simple">
class Extend(EnumDict):
    DICT = {AsDict, }
    PROXY = {DataProxy, }
    ALL = {AsDict, DataProxy, }


class Simple(types.SimpleNamespace):
    @classmethod
    def simple(cls, name: Any, _extend: Extend = Extend.DICT, **kwargs) -> Any:
        """
        Creates a New Simple Namespace Sub Class.

        Default returns a Simple Namespace with `AsDict` base.

        Warnings:
            Call `extend` as positional argument.

        Args:
            name: class name or Namespace Sub Class.
            _extend: add to default bases.
            **kwargs: kwargs

        Raises:
            ValueError: ValueError

        Returns:
            Any:
        """
        if isinstance(name, str):
            if (_extend := kwargs.get('_extend', _extend)) is not _extend:
                del kwargs['_extend']
            name = types.new_class(name, bases=tuple({*Extend.DICT.value, *_extend.value, cls, }))
            if not kwargs:
                return name

        if kwargs:
            return name(**kwargs)
        else:
            raise ValueError(f'kwargs: must be provided for cls: {name}.')


# </editor-fold>

# <editor-fold desc="System">
@dataclasses.dataclass
class System(Distro, Executable, Machine, Py):
    """Distro, Executable/Commands Installed, Server OS, Platform and Python Information Class."""
    pass


# </editor-fold>

# <editor-fold desc="Package">
@dataclasses.dataclass
class Package(AsDict):
    filename: Union[Path, str] = _path_installed.filename
    parameter: str = str()
    _version: str = str()
    bapy_imported: bool = datafield(default=_imported, init=False)
    env: Env = datafield(default=None, init=False)
    env_file: Path = datafield(default=None, init=False)
    github: GitHub = datafield(default=None, init=False)
    home: Path = datafield(default=_path_installed.home, init=False)
    installed: bool = datafield(default=_path_installed.installed, init=False)
    ic: icecream.IceCreamDebugger = datafield(default=None, init=False)
    ic_enabled: icecream.IceCreamDebugger = datafield(default=None, init=False)
    kill: Kill = datafield(default=None, init=False)
    log: LogR = datafield(default=None, init=False)
    log_dir: Path = datafield(default=_path_installed.log_dir, init=False)
    log_file: Path = datafield(default=_path_installed.log_file, init=False)
    mongo: Path = datafield(default=_path_installed.mongo, init=False)
    name: str = datafield(default=_path_installed.name, init=False)
    path: Path = datafield(default=_path_installed.path, init=False)
    prefix: str = datafield(default=_path_installed.prefix, init=False)
    repo: str = datafield(default=_path_installed.repo, init=False)
    project: Path = datafield(default=_path_installed.project, init=False)
    user: str = datafield(default=User.name, init=False)
    work: Path = datafield(default=_path_installed.work, init=False)

    def __post_init__(self):
        self.filename = Path(self.filename)
        self.env = Env(prefix=self.prefix)
        self.env_file = self.env.file
        p_i = path_installed(self.filename)
        self.home = p_i.home
        self.installed = p_i.installed
        self.ic = icc
        self.ic.enabled = self.ic_enabled = self.env.ic.value
        self.log_dir = p_i.log_dir
        self.log_file = p_i.log_file
        self.mongo = p_i.mongo
        self.name = p_i.name
        self.path = p_i.path
        self.prefix = p_i.prefix
        self.repo = p_i.repo
        self.project = p_i.project
        self.work = p_i.work
        self.log = LogR.get_log(name=self.name, p=self.log_file, file=self.env.log_level_file.value,
                                stream=self.env.log_level.value, installed=self.installed)
        self.github = GitHub(path=self.project if not self.installed else None, log=self.log.child)
        self.kill = Kill(command=self.name, log=self.log.child, parameter=self.parameter)
        atexit.register(self.kill.exit)
        # TODO
        # self.log.info('Changed: package', f'{self.filename=}', f'{self.parameter=}', f'{self.version=}',
        #               fm(self.asdict))

    @property
    def version(self) -> Optional[str]:
        try:
            return self._version if self._version else importlib.metadata.version(self.name)
        except importlib.metadata.PackageNotFoundError:
            pass

    @version.setter
    def version(self, value: str):
        self._version = value


_log.info('Package.defaults()', fm(Package.defaults()))
bapy = Package(filename=__file__, _version='0.22.12')


# </editor-fold>


# <editor-fold desc="Exceptions">
class BapyException(Exception):
    """Custom base class for all Repo exception types."""


class BapyFrameBackBack(BapyException):
    def __init__(self, message):
        self.message = message


class BapyGitDirectoryIsDirty(BapyException):
    def __init__(self, message):
        self.message = message


class BapyInvalidIP(BapyException):
    def __init__(self, ip):
        self.ip = ip
        self.message = f'Invalid IP: {self.ip}'


# </editor-fold>

# <editor-fold desc="Echo">
@app.command(context_settings=context)
def black(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Black.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='black', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def red(msg: str, bold: bool = False, underline: bool = False,
        blink: bool = False, err: bool = True, e: bool = True) -> None:
    """
    Red.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='red', err=err)
    if e:
        sys.exit(1)


@app.command(context_settings=context)
def green(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Green.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='green', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def yellow(msg: str, bold: bool = False, underline: bool = False,
           blink: bool = False, err: bool = True, e: bool = False) -> None:
    """
    Yellow.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='yellow', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def blue(msg: str, bold: bool = False, underline: bool = False,
         blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Blue.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='blue', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def magenta(msg: str, bold: bool = False, underline: bool = False,
            blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Magenta.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='magenta', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def cyan(msg: str, bold: bool = False, underline: bool = False,
         blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Cyan.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='cyan', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def white(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    White.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='white', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def bblack(msg: str, bold: bool = False, underline: bool = False,
           blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Black.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_black', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def bred(msg: str, bold: bool = False, underline: bool = False,
         blink: bool = False, err: bool = True, e: bool = True) -> None:
    """
    Bred.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_red', err=err)
    if e:
        sys.exit(1)


@app.command(context_settings=context)
def bgreen(msg: str, bold: bool = False, underline: bool = False,
           blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bgreen.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_green', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def byellow(msg: str, bold: bool = False, underline: bool = False,
            blink: bool = False, err: bool = True, e: bool = False) -> None:
    """
    Byellow.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_yellow', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def bblue(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bblue.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_blue', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def bmagenta(msg: str, bold: bool = False, underline: bool = False,
             blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bmagenta.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_magenta', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def bcyan(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bcyan.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_cyan', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def bwhite(msg: str, bold: bool = False, underline: bool = False,
           blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bwhite.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_white', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=context)
def reset(msg: str = str(), bold: bool = False, underline: bool = False, blink: bool = False, err: bool = False,
          e: bool = False) -> None:
    """
    Reset.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='reset', err=err)
    if e:
        sys.exit(0)


# </editor-fold>

# <editor-fold desc="Functions">
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


async def acprint(*args, **kwargs):
    await executor(cprint, *args, **kwargs)


async def aiocmd(command: Union[str, list], decode: bool = True, utf8: bool = False,
                 lines: bool = False) -> Union[CmdOut, int, list, str]:
    """
    Asyncio run cmd.

    Args:
        command: command.
        decode: decode and strip output.
        utf8: utf8 decode.
        lines: split lines.

    Returns:
        Union[CmdOut, int, list, str]: [stdout, stderr, proc.returncode].
    """
    proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE, loop=asyncio.get_running_loop())
    stdout, stderr = await proc.communicate()
    if decode:
        stdout = stdout.decode().rstrip('.\n')
        stderr = stderr.decode().rstrip('.\n')
    elif utf8:
        stdout = stdout.decode('utf8').strip()
        stderr = stderr.decode('utf8').strip()

    out = stdout.splitlines() if lines else stdout

    return CmdOut(out, stderr, proc.returncode)


def aioloopid():
    try:
        return asyncio.get_running_loop()._selector
    except RuntimeError:
        return None


def aioloop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None


def aiorun(call, *, debug=False):
    if loop := aioloop():
        if not asyncio.coroutines.iscoroutine(call):
            raise ValueError("a coroutine was expected, got {!r}".format(call))

        try:
            loop.set_debug(debug)
            return loop.run_until_complete(call)
        finally:
            try:
                asyncio.runners._cancel_all_tasks(loop)
                loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                asyncio.events.set_event_loop(None)
                loop.close()
    else:
        return asyncio.run(call)


def aiowrap(func):
    @functools.wraps(func)
    async def aio_run(*args, **kwargs):
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    @functools.wraps(func)
    def run(*args, **kwargs):
        return func(*args, **kwargs)

    if loop := aioloop():
        return aio_run
    return run


@app.command(context_settings=context)
def appdir(stdout: bool = False) -> None:
    """
    CLI/APP dir.

    Args:
        stdout: stdout.

    Returns:
        None:
    """
    if stdout:
        green(typer.get_app_dir(Path(__file__).parent.text))
    else:
        return green(typer.get_app_dir(Path(__file__).parent.text))


@app.command(context_settings=context)
def ask(msg: str) -> bool:
    """
    Ask Yes or No.

    Args:
        msg: text message.

    Returns:
        bool:
    """
    from rich.prompt import Prompt
    if Prompt.ask(msg, choices=['Yes', 'No'], default='Yes') == 'Yes':
        return True
    return False


@app.command(context_settings=context)
def base64auth(username: str, password: str, stdout: bool = False) -> str:
    """
    Generates a base64 auth for usage with .npmrc.

    Args:
        username: user name.
        password: user password.
        stdout: stdout.

    Returns:
        Str: openssl base64.
    """
    rv = os.popen(f'echo -n "{username}:{password}" | openssl base64').read().splitlines()[0]
    if stdout:
        console.print(rv)
    return rv


@functools.singledispatch
def clean_empty(obj: Any) -> Any:
    """
    Clean empty keys in nested dict.

    isinstance() checks are taken care of by @singledispatch based on the type annotations of the registered functions.

    Any values set to numeric 0 (integer 0, float 0.0) will also be cleared. Numeric 0 values can be retained
    with if v or v == 0.

    Args:
        obj:

    Returns:

    """
    return obj


@clean_empty.register
def _dicts(d: dict) -> dict:
    items = ((k, clean_empty(v)) for k, v in d.items())
    return {k: v for k, v in items if v}


@clean_empty.register
def _lists(l: list) -> list:
    items = map(clean_empty, l)
    return [v for v in items if v]


@clean_empty.register
def _sets(l: set) -> set:
    items = map(clean_empty, l)
    return {v for v in items if v}


def click_custom_startswith(string: str, incomplete: str) -> bool:
    """
    A custom completion matching that supports case insensitive matching.

    Args:
        string: string
        incomplete: incomplete

    Returns:
        bool:
    """
    case_insensitive_completion: str = '_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE'

    if os.environ.get(case_insensitive_completion):
        string = string.lower()
        incomplete = incomplete.lower()
    return string.startswith(incomplete)


click_completion.core.startswith = click_custom_startswith


def cmd(command: Iterable, shell: bool = True, sysexec: bool = False,
        lines: bool = True) -> Union[CmdOut, int, list, str]:
    """
    Runs a cmd.

    Examples:
        >>> cmd('ls a')
        ([], ['ls: a: No such file or directory'], 1)
        >>> assert 'Requirement already satisfied' in cmd('pip install pip', sysexec=True)[0][0]
        >>> cmd('ls a', shell=False, lines=False)  # Extra '\' added to avoid docstring error.
        ('', 'ls: a: No such file or directory\\n', 1)
        >>> cmd('echo a', lines=False)  # Extra '\' added to avoid docstring error.
        'a\\n'

    Args:
        command: command.
        shell: expands shell variables and one line (shell True expands variables in shell).
        sysexec: runs with sys executable.
        lines: split lines so ``\\n`` is removed from all lines (extra '\' added to avoid docstring error).

    Returns:
        Union[CmdOut, int, list, str]:
    """
    if sysexec:
        command = f'{sys.executable} -m {command}'
    elif not shell:
        command = shlex.split(command)

    if lines:
        text = False
    else:
        text = True

    proc = subprocess.run(command, shell=shell, capture_output=True, text=text)

    def rv(out=True):
        if out:
            if lines:
                return proc.stdout.decode("utf-8").splitlines()
            else:
                # return proc.stdout.decode("utf-8").rstrip('.\n')
                return proc.stdout
        else:
            if lines:
                return proc.stderr.decode("utf-8").splitlines()
            else:
                # return proc.stderr.decode("utf-8").rstrip('.\n')
                return proc.stderr

    return CmdOut(rv(), rv(False), proc.returncode)


def cmd_completion(cls, append, case_insensitive, p):
    def provide_default():
        if os.name == 'posix':
            return os.path.basename(os.environ['SHELL'])
        elif os.name == 'nt':
            return os.path.basename(os.environ['COMSPEC'])
        raise NotImplementedError(f'OS {os.name!r} support not available')

    try:
        shell = shellingham.detect_shell()
    except shellingham.ShellDetectionFailure:
        shell = provide_default()

    extra_env = {cls.case_insensitive_completion: 'ON OFF'} if case_insensitive else {}
    shell, p = click_completion.core.install(shell=shell, path=p, append=append, extra_env=extra_env)
    click.echo(f'{shell} completion installed in {p}')


@app.command(context_settings=context)
def confirmation(msg: str) -> bool:
    """
    Ask for Yes/no and confirmation.

    Args:
        msg: text message.

    Returns:
        bool:
    """
    if ask(msg):
        are_you_sure = rich.prompt.Confirm.ask(f'Are you sure?')
        assert are_you_sure
        return True
    return False


def datafactory(data: Union[dict, list, collections.OrderedDict, set]) -> \
        Union[dict, list, collections.OrderedDict, set]:
    return data


def datafactorytype(cls, field) -> Any:
    """
    Default factory for dataclass field with type.

    Args:
        cls:
        field:

    Returns:
        Any:
    """
    for attr in dataclasses.fields(cls):
        if attr.name == field:
            return attr.type()


def default_dict(factory: Optional[Callable] = None, init: Any = None, /, *args, **kwargs) -> defaultdict:
    value = init(*args, **kwargs) if callable(init) else init
    if factory and value is None:
        value = factory()
    elif value is None:
        return collections.defaultdict(factory)
    return collections.defaultdict(factory, value)


def del_key(data: dict, key: Iterable = ('self', 'cls',)) -> dict:
    d = data.copy()
    for item in iter_split(key):
        with suppress(KeyError):
            del d[item]
    return d


def dict_exclude(data: dict, exclude: Union[list, tuple] = None) -> Optional[dict]:
    """
    Dict with vars in `exclude`. Default: private vars.

    Args:
        data: input dict.
        exclude: vars to exclude.

    Example:
        >>> import inspect
        >>>
        >>> new_dict = dict_include(inspect.stack(2)[0].frame.f_locals, include=('__annotations__', ))

    Returns:
        Optional[dict]:
    """
    if exclude:
        return {key: value for key, value in data.items() if key != exclude}
    else:
        return {key: value for key, value in data.items() if key[:1] != '_'}


def dict_include(data: dict, include: Union[list, tuple] = None) -> Optional[dict]:
    """
    Dict with vars in `include`. Default: ``(str, int, tuple, set, list, bool, float, dict)``.

    Example:
        >>> import inspect
        >>>
        >>> new_dict = dict_include(inspect.stack(2)[0].frame.f_globals)

    Args:
        data: input dict.
        include: vars to include.

    Returns:
        Optional[dict]:
    """
    if include:
        return {key: value for key, value in data.items() if key in include}
    else:
        return {key: value for key, value in data.items()
                if key[:1] != '_' and type(value) in (str, int, tuple, set, list, bool, float, dict)}


def distribution(p: str = str(), stdout: bool = False) -> importlib.metadata.Distribution:
    """
    Package/Project Distribution Information.

    Args:
        p: package
        stdout: stdout

    Returns:
        importlib_metadata.Distribution:
    """
    try:
        rv = importlib.metadata.distribution(p if p else _path_installed.name)
        if stdout:
            console.print(rv)
        return rv
    except importlib.metadata.PackageNotFoundError as exc:
        _log.debug(fm(exc))


def dump_ansible_yaml(p: Any, data: dict):
    """
    Dump yaml with ansible format.

    Args:
        p: path
        data: data
    """
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=2, sequence=2, offset=2)
    # yaml.compact(seq_seq=False, seq_map=False)
    yaml.dump(data, p.open('w+'))


async def executor(func: Any, *args: Any, pool: Optional[Executor] = None, **kwargs: Any) -> Any:
    """
    Run in :lib:func:`loop.run_in_executor` with :class:`concurrent.futures.ThreadPoolExecutor`,
        :class:`concurrent.futures.ProcessPoolExecutor` or
        :lib:func:`asyncio.get_running_loop().loop.run_in_executor` or not poll.

    Args:
        func: func
        *args: args
        pool: pool
        **kwargs: kwargs

    Raises:
        ValueError: ValueError

    Returns:
        Awaitable:
    """
    loop = asyncio.get_running_loop()
    call = partial(func, *args, **kwargs)
    if not func:
        raise ValueError

    if pool:
        with pool.value() as p:
            return await loop.run_in_executor(p, call)
    return await loop.run_in_executor(pool, call)


def flat_list(l: Iterable, recurse: bool = False, unique: bool = False, sort: bool = True) -> Union[list, Iterable]:
    """
    Flattens an Iterable

    Args:
        l: iterable
        recurse: recurse
        unique: when recurse
        sort: sort

    Returns:
        Union[list, Iterable]:
    """
    if unique:
        recurse = True

    flat = []
    _ = [flat.extend(flat_list(item, recurse, unique) if recurse else item)
         if isinstance(item, list) else flat.append(item) for item in l if item]
    if unique:
        rv = list(set(flat))
        return sorted(rv) if sort else rv
    return sorted(flat) if sort else flat


def force_async(fn):
    """
    Turns a sync function to async function using threads.
    """
    from concurrent.futures import ThreadPoolExecutor
    import asyncio
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(fn):
    """
    Turn an async function to sync function.
    """
    import asyncio

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper


def get_all(obj: dict, get: GetAll = GetAll.KEYS, generator: bool = False) -> Iterable:
    # noinspection PyUnresolvedReferences
    """
    All keys or values of nested dict or List.

    Examples:
        >>> data = dict(key1=dict(key2=dict(key3=dict(key4='value1'))))
        >>> keys = tuple(item for item in get_all(data))
        >>> keys
        ('key1', 'key2', 'key3', 'key4')
        >>> values = tuple(item for item in get_all(data, GetAll.VALUES))
        >>> values
        ('value1',)

    Args:
        obj: obj
        get: get
        generator: generator or return

    Raises:
        ValueError: ValueError

    Yields:
        Iterable:
    """

    def _get_all(o, g):
        if isinstance(o, dict):
            for key, value in o.items():
                if g is GetAll.KEYS:
                    yield key
                elif g == GetAll.VALUES:
                    if not (isinstance(value, dict) or isinstance(value, list)):
                        yield value
                else:
                    raise ValueError('`GetAll.KEYS` or `GetAll.VALUES`')
                for ret in _get_all(value, g=g):
                    yield ret
        elif isinstance(o, list):
            for el in o:
                for ret in _get_all(el, g=g):
                    yield ret

    if generator:
        return _get_all(obj, get)
    return [item for item in _get_all(obj, get)]


def get_choice_class(data: Union[Iterable, GenericAlias], case_sensitive: bool = True) -> click.Choice:
    """
    :class:`click.Echo` from different data sources.

    Examples:
        >>> choice = get_choice_class(Literal['a'])
        >>> choice
        Choice('['a']')
        >>> choice = get_choice_class(choice.choices)
        >>> choice
        Choice('['a']')
        >>> choice = get_choice_class(''.join(choice.choices))
        >>> choice
        Choice('['a']')

    Args:
        data: data
        case_sensitive: case_sensitive

    Returns:
        click.Choice:
    """
    if isinstance(data, GenericAlias):
        data = data.__args__
    elif isinstance(data, str):
        data = data.split()
    return click.Choice(data, case_sensitive)


# noinspection StrFormat
def gen_key(home: Any = None, private: Any = None, public: Any = None, text: Any = None,
            email: Any = None):
    """
    Gpg key generation and exporting public and private keys.

    Args:
        home: gpg home path
        private: gpg private dest path
        public: gpg public dest path
        text: render template
        email: author email
    """
    home = shlex.quote(str(home))
    private = shlex.quote(str(private))
    public = shlex.quote(str(public))
    text = shlex.quote(str(text))
    email = shlex.quote(email)

    with shell_proc.Shell(stdout=sys.stdout, stderr=sys.stderr, blocking=False) as sh:
        sh(
            f'mkdir -p {home}; chmod go-rwx {home}; '
            f'rm -rf {home}/*; '
            f'rm -rf {private} {public}; '
            f'gpg --homedir {home} --batch --gen-key {text}; '
            f'gpg --homedir {home} --export --armor --output {public} {email};'
            f'gpg --homedir {home} --export-secret-key --armor {email} > {private}; '
            f'sudo rm -rf {home}/S.gpg-agent*;'
        )

    time.sleep(1)
    print('1 Second has passed', 'Running:', sh.current_command)
    time.sleep(1)
    print('2 Seconds have passed', 'Running:', sh.current_command)
    time.sleep(1)
    print('3 Seconds have passed', 'Running:', sh.current_command)

    sh.wait()

    table = '|{:_<20}|{:_<20}|{:_<20}|{:_<50}|'
    print(table.format(str(), str(), str(), str()).replace('|', '_'))
    print(table.format("Exit Code", "Has Error", "Has Output", "Command").replace('_', ' '))
    print(table.format(str(), str(), str(), str()))
    for item in sh.history:
        print(table.format(item.exit_code, item.has_error(), item.has_output(), item.cmd).replace('_', ' '))
    print(table.format(str(), str(), str(), str()).replace('|', '_'))


def get_context(variables=str()):
    locals_context_dict = sys._getframe(2).f_locals
    if locals_context_dict.get('l'):
        del locals_context_dict['l']

    if locals_context_dict.get('cls'):
        del locals_context_dict['cls']
    aiotask_context_dict = {}
    try:
        # noinspection PyUnresolvedReferences
        aiotask_context_dict = {key: asyncio.current_task().get(key) for key in asyncio.current_task()}
    except (RuntimeError, AttributeError, NameError,):
        pass

    context_dict = {**locals_context_dict, **aiotask_context_dict, **sys._getframe(2).f_globals}
    context_dict_clean = {key: context_dict.get(key) for key in context_dict if not_(key)
                          and is_data(context_dict.get(key))}
    if variables:
        try:
            msg_dict = {var: str() for var in variables.split() if not context_dict_clean.get(var, None)}
            variables_dict = {var: eval(var, context_dict_clean, msg_dict) for var in variables.split()
                              if not_(var) and is_data(eval(var, context_dict, msg_dict))}
        except (AttributeError, NameError, KeyError):
            pass
        else:
            context_dict_clean = variables_dict
    else:
        if context_dict_clean.get('self', None):
            add = {'self': context_dict_clean['self']}
            context_dict_clean = {**context_dict_clean, **add}
    final = {**context_dict_clean}
    msg = ", ".join("{}: {}".format(key, value) for key, value in {
        var.replace("\\", ""): vars(final.get(var))
        if getattr(final.get(var), '__dict__', None) and var[:1] != '_'
        else final.get(var) for var in list(final)
    }.items() if not_(key) and is_data(key))
    # exception = sys.exc_info()[1]
    # if exception:
    #     exception.args = ('{} [{}]'.format(exception.args[0], msg) if exception.args else msg,) + exception.args[1:]
    return msg


def get_key(data: dict, value: Any) -> Any:
    """
    Get Dict Key from Value.

    Args:
        data: data
        value: value

    Returns:
        Any:
    """
    for key, val in data.items():
        if val == value:
            return key


def get_vars_docs(fname: str) -> dict:
    """
    Read the module referenced in fname (often <module>.__file__) and return a
    dict with global variables, their value and the "docstring" that follows
    the definition of the variable.

    Args:
        fname: fname

    Returns:
        dict:
    """
    file = os.path.splitext(fname)[0] + '.lib'  # convert .pyc to .lib
    with open(file, 'r') as f:
        fstr = f.read()
    rv = {}
    key = None
    for node in ast.walk(ast.parse(fstr)):
        if isinstance(node, ast.Assign):
            key = node.targets[0].id
            rv[key] = [node.value.id, str()]
            continue
        elif isinstance(node, ast.Expr) and key:
            rv[key][1] = node.value.s.strip()
        key = None
    return rv


@app.command(context_settings=context)
def info(dist: str = str(), executable: bool = False, linux: bool = False,
         machine: bool = False, project: bool = False, py: bool = False, user: bool = False) -> None:
    """
    Command to provide info.

    Args:
        dist: importlib distribution.
        executable: executables in server.
        linux: linux distribution.
        machine: machine information.
        project: package and path information.
        py: python information.
        user: user data.
    """
    if not (bool(dist) | executable | linux | machine | project | py | user):
        executable = linux = machine = project = py = user = True
        dist = dist if dist else _path_installed.repo

    if dist:
        d = distribution(dist)
        console.print('[bold blue]Distribution: ', Obj(d).asdict, '\n', '[bold blue]Metadata: ', metadata(dist), str())
    if executable:
        console.print('[bold blue]Executable: ', dataclasses.asdict(Executable()), str())
    if linux:
        console.print('[bold blue]Distro: ', dataclasses.asdict(Distro()), str())
    if machine:
        console.print('[bold blue]Machine: ', dataclasses.asdict(Machine()), str())
    if project:
        console.print('[bold blue]Path: ', bapy.asdict, str())
    if py:
        console.print('[bold blue]Py: ', dataclasses.asdict(Py()), str())
    if user:
        console.print('[bold blue]User: ', dataclasses.asdict(User()), str())


@functools.cache
def ipaddr(ip: Optional[IPAddressLike] = None, loc: Union[IPLoc, bool] = False, log: LogR = _log) -> IPvType:
    """
    Take an IP string/int and return an object of the correct type.

    Args:
        ip: A string or integer, the IP address.  Either IPv4 or IPv6 addresses may be supplied; integers
            less than 2**32 will be considered to be IPv4 by default. Default to my ip.
        loc: Add location info.
        log: log.

    Returns:
        IPvType:

    Raises:
        ValueError: if the *address* passed isn't either a v4 or a v6
          address

    """
    ip = ip if ip else ipmine()

    if ip:
        # noinspection PyArgumentList
        loc = loc if isinstance(loc, IPLoc) else iploc(ip) if loc else IPLoc()

        try:
            return IPv4(ip, loc, log)
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            pass

        try:
            return IPv6(ip, loc, log)
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            pass

        raise ValueError(f'{ip} does not appear to be an IPv4 or IPv6 address')
    else:
        log.warning(f'{ip=}', f'{log=}')


async def ipaddr_aio(ip: Optional[IPAddressLike] = None, loc: Union[IPLoc, bool] = False, log: LogR = _log) -> IPvType:
    return await asyncio.to_thread(ipaddr, ip, loc, log)


@functools.cache
@retry_decorator.retry(urllib.error.HTTPError, tries=3, timeout_secs=2, logger=_log)
def ipmine() -> IPvType:
    """
    My IP.

    Returns:
        IPvType: ip.
    """
    return ipaddr(ip) if (ip := urllib.request.urlopen('https://ident.me').read().decode('utf8')) else ipaddr(localhost)


async def ipmine_aio() -> str:
    """
    My IP.

    Returns:
        str: ip.
    """
    return await asyncio.to_thread(ipmine)


@functools.cache
@retry_decorator.retry(urllib.error.HTTPError, tries=3, timeout_secs=10, logger=_log)
def iploc(ip: IPAddressLike = None) -> IPLoc:
    """
    IP location info.

    Args:
        ip: default my ip.

    Returns:
        IPLoc:
    """
    with urllib.request.urlopen(f'https://geolocation-db.com/json/697de680-a737-11ea-9820-af05f4014d91/'
                                f'{str(ip) if ip else ipmine()}') as loc:
        # noinspection PyArgumentList
        return IPLoc(*[loc.get(item) for item in IPLoc._fields]) if (
            loc := json.loads(loc.read().decode())) else IPLoc()


async def iploc_aio(ip: str = None) -> IPLoc:
    return await asyncio.to_thread(iploc, ip)


def is_data(obj) -> bool:
    def exclude():
        for module in [typing, ]:
            if module is inspect.getmodule(obj):
                return True
        if 'wrapper' in str(type(obj)) or ('__' in str(obj) and '__main__' not in str(obj)):
            return True
        return False

    return not \
        inspect.isabstract(obj) | inspect.isroutine(obj) | inspect.iscode(obj) | inspect.isframe(obj) | \
        inspect.istraceback(obj) | inspect.isawaitable(obj) | inspect.iscoroutine(obj) | inspect.isgenerator(obj) | \
        inspect.isasyncgen(obj) | inspect.isasyncgenfunction(obj) | inspect.iscoroutinefunction(obj) | \
        inspect.isgeneratorfunction(obj) | inspect.isgetsetdescriptor(obj) | inspect.isdatadescriptor(obj) | \
        inspect.ismodule(obj) | inspect.isclass(obj) | exclude()


@app.command(context_settings=context)
def is_pip(stdout: bool = False) -> bool:
    """
    Checks if pip is installed.

    Args:
        stdout: stdout.

    Returns:
        bool
    """
    try:
        # noinspection PyCompatibility
        import pip
        if stdout:
            green(str(True))
        return True
    except ModuleNotFoundError:
        if stdout:
            red(str(False))
        return False


def iter_split(data: Iterable) -> Any:
    """
    Item str().split() and Iterables.

    Args:
        data: data

    Raises:
        TypeError: TypeError

    Returns:
        Any:
    """
    if isinstance(data, Iterable):
        if isinstance(data, str):
            return data.split() if ' ' in data else [data]
        return data
    else:
        raise TypeError(f'{data=} must be iterable.')


def list_utils(list_: [list, tuple] = None, option: ListUtils = ListUtils.LOWER) -> list:
    return [getattr(item, option.lower)() for item in list_]


def literal(data, index: int = None) -> Union[list[str], str]:
    if index is None:
        return list(data.__args__)
    return data.__args__[index]


def load_modules(p) -> None:
    """
    Load Modules of Package.

    Args:
        p: package.
    """
    p = p if p else _path_installed.name
    p._modules = []

    pkgname = p.__name__
    pkgpath = Path(p.__file__).parent

    # noinspection PyTypeChecker
    for mod in pkgutil.iter_modules([pkgpath]):
        modulename = pkgname + '.' + mod[1]
        __import__(modulename, locals(), globals())
        module = sys.modules[modulename]

        module._package = p
        # module._packageName = pkgname

        p._modules.append(module)
        if Path(module.__file__).parent == pkgpath:
            module._isPackage = False
        else:
            module._isPackage = True
            # noinspection PyTypeChecker,PydanticTypeChecker
            load_modules(module)


def mapped_commands(command_map: dict) -> Any:
    """
    Commands mapping.

    Args:
        command_map: command_map

    Returns:
        Any:
    """

    class CommandGroup(click.Group):
        def get_command(self, ctx, cmd_name):
            for real_command, aliases in command_map.items():
                if cmd_name in aliases:
                    return click.Group.get_command(self, ctx, real_command)
            return None

        def list_commands(self, ctx):
            return [a for b in command_map.values() for a in b]

    return CommandGroup


def metadata(p: str = str(), stdout: bool = False) -> mailbox.Message:
    """
    Package/Project Metadata Information.

    Args:
        p: package
        stdout: stdout
    Returns:
        dict:
    """
    try:
        rv = importlib.metadata.metadata(p if p else _path_installed.name)
        if stdout:
            console.print(rv)
        return rv
    except importlib.metadata.PackageNotFoundError as exc:
        _log.debug(fm(exc))


def mod_name(mod):
    return mod.__name__.rpartition('.')[-1]


def move_to_key(mydict: dict, new_key: str, keys_to_move: Union[list, tuple]):
    if set(mydict.keys()).intersection(keys_to_move):
        mydict[new_key] = {}
        for k in keys_to_move:
            mydict[new_key][k] = mydict[k]
            del mydict[k]


def namedtuple(typename: Any, fields: Union[list, str, tuple] = None, defaults: tuple = None,
               fieldtype: Any = str) -> Any:
    """
    Makes a new typing `collections.namedtuple`.

    Examples:
        >>> domain_fields: tuple = ('company', 'server', )
        >>> Domain = namedtype('Domain', domain_fields)
        >>> assert 'Domain' in str(Domain)
        >>> domain_values: tuple = ('nference.net', 'nferx.com', )
        >>> domain: Domain = namedtuple('Domain', domain_fields, defaults=domain_values)
        >>> domain
        Domain(company='nference.net', server='nferx.com')
        >>> assert 'Domain' in str(type(domain))
        >>> dir_names: tuple = 'download', 'generated',
        >>> # noinspection PyUnresolvedReferences
        >>> dir_defaults: tuple = tuple(Path('/tmp') / item for item in dir_names)
        >>> dir_defaults
        (Path('/tmp/download'), Path('/tmp/generated'))
        >>> dirs = namedtuple('TmpDir', dir_names, dir_defaults, Path)
        >>> dirs
        TmpDir(download=Path('/tmp/download'), generated=Path('/tmp/generated'))
        >>> assert'TmpDir' in str(type(dirs))

    Args:
        typename: Named Tuple Yyping Name.
        fields: Named Tuple Field Names.
        fieldtype: Named Tuple Fields typing.
        defaults: Creates Named Tuple with defaults values.

    Returns:
        Any: new typing `collections.namedtuple`.
    """
    fields = fields.split() if isinstance(fields, str) else fields
    typename = namedtype(typename, fields, fieldtype) if isinstance(typename, str) else typename
    TypeNameDefaults: typename = collections.namedtuple(typename.__name__, typename._fields, defaults=defaults)
    name_defaults: typename = TypeNameDefaults()
    return name_defaults


def namedtype(typename, fields: Union[list, str, tuple], fieldtype: Any = str) -> Any:
    """
    Returns a typing NamedTuple associating fieldtype to fields.

    Examples:
        >>> domain_fields: tuple = ('company', 'server', )
        >>> Domain = namedtype('Domain', domain_fields)
        >>> assert 'Domain' in str(Domain)
        >>> type(Domain)
        <class 'type'>
        >>> home_dir_names: tuple = ('download', 'generated', 'github', 'log', 'tmp', )
        >>> HomeDir = namedtype('HomeDir', home_dir_names, Path)
        >>> assert 'HomeDir' in str(HomeDir)
        >>> type(HomeDir)
        <class 'type'>

    Args:
        typename: Named Tuple Typing Name.
        fields: Named Tuple Field Names.
        fieldtype: Named Tuple Fields typing.

    Returns:
        Any: new typing `collections.namedtuple`.
    """
    fields = fields.split() if isinstance(fields, str) else fields
    return typing.NamedTuple(typename, **{item: fieldtype for item in fields})


def not_(name: str) -> bool:
    """
    Is not private?

    Args:
        name: name

    Returns:
        bool:
    """
    return name[:1] != '_'


def other(data: Union[list, set, tuple], value: Any) -> Any:
    """
    Get The Other Value.

    Args:
        data: data
        value: value

    Returns:
        Any:
    """
    return data[0] if data[1] == value else data[1]


@app.command(context_settings=context, name='package')
def _package():
    """Package."""
    bapy.ic.enabled = True
    bapy.ic(Package.defaults(), bapy.asdict)


def package_info(p: str = str(), stdout: bool = False) -> tuple[bool, str, str]:
    """
    Check if installed version of package is the latest.

    Args:
        p: package name.
        stdout: stdout.

    Returns:
        tuple[bool, str, str]: [``upgrade_version`` upgrade version current != latest, ``current_version``,
            ``latest_version``].
    """
    p = p if p else _path_installed.name
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(p)],
                                        capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:') + 15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ', '').split(',')[-1]

    current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(p)],
                                         capture_output=True, text=True))
    current_version = current_version[current_version.find('Version:') + 8:]
    current_version = current_version[:current_version.find('\\n')].replace(' ', '')

    upgrade_version = False if latest_version == current_version else True
    if stdout:
        console.print(upgrade_version, current_version, latest_version)
    return upgrade_version, current_version, latest_version


@app.command(context_settings=context)
def package_latest(p: str = str(), stdout: bool = False) -> str:
    """
    Latest version of package using pip install random as version.

    Args:
        p: package.
        stdout: stdout.

    Returns:
        Str: latest_version.
    """
    p = p if p else _path_installed.name
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(p)],
                                        capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:') + 15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ', '').split(',')[-1]
    if stdout:
        console.print(latest_version)
    return latest_version


@app.command(context_settings=context)
def package_latest_search(p: str = str(), stdout: bool = False) -> str:
    """
    Latest version of package using pip search.

    Args:
        p: package.
        stdout: stdout.

    Returns:
        Str: latest_version.
    """
    p = p if p else _path_installed.name
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'search', p], capture_output=True, text=True))
    text = f'{p} ('
    latest_version = latest_version[latest_version.find(text) + len(text):]
    latest_version = latest_version[:latest_version.find(')')]
    if stdout:
        console.print(latest_version)
    return latest_version


plural = inflect.engine().plural


def prefix_suffix(string: str, fix: str, add: bool = True, prefix: bool = True, separator: str = '_') -> str:
    """
    Adds or removes prefix with separator from string.

    Examples:
        >>> from bapy import prefix_suffix
        >>> prefix_suffix('open', 'scan')
        'scan_open'
        >>> prefix_suffix('open', 'scan', prefix=False)
        'open_scan'
        >>> prefix_suffix('scan_open', 'open', add=False, prefix=False)
        'scan'

    Args:
        string: To add or remove.
        fix: prefix or suffix.
        add: add prefix/suffix or remove.
        prefix: True for prefix and False for suffix.
        separator: separator between prefix/suffix and string.

    Returns:

    """
    if add:
        return f'{fix}{separator}{string}' if prefix else f'{string}{separator}{fix}'
    return string.removeprefix(f'{fix}{separator}') if prefix else string.removesuffix(f'{separator}{fix}')


def print_modules(p: str):
    p = p if p else _path_installed.name
    p = importlib.import_module(p)
    # noinspection PydanticTypeChecker
    console.print(mod_name(p))
    # noinspection PyUnresolvedReferences
    for mod in p._modules:
        if mod._isPackage:
            print_modules(mod)
        else:
            # noinspection PyCallingNonCallable
            console.print(mod_name(mod))


@app.command(context_settings=context)
def pypifree(name: str, stdout: bool = False) -> bool:
    """
    Pypi name available.

    Examples:
        >>> assert pypifree('common') is False
        >>> assert pypifree('sdsdsdsd') is True

    Args:
        name: package.
        stdout: stdout.

    Returns:
        bool: True if available.
    """
    r = requests.get(f'https://pypi.org/pypi/{name}/json')

    if r:
        if stdout:
            red('Taken')
        return False
    else:
        if stdout:
            green('Available')
        return True


def rename_keys(mydict: dict, rename_map: dict) -> dict:
    for current_name, new_name in rename_map.items():
        if mydict.get(current_name) is not None:
            mydict[new_name] = mydict[current_name]
            del mydict[current_name]
    return mydict


def reverse_dict(data: dict) -> dict:
    """
    Reverse a Dict.

    Args:
        data: data

    Returns:
        dict:
    """
    keys_list = list(map(lambda k: k, data))
    reverse_key_list = keys_list[::-1]
    reverse_d = dict()
    i = 0
    while i < len(reverse_key_list):
        key = reverse_key_list[int(i)]
        reverse_d[key] = data[key]
        i += 1
    if len(reverse_d) > 0:
        return reverse_d


@app.command(context_settings=context)
def secrets():
    """Secrets Update."""
    dist = distro.LinuxDistribution().info()['id']
    if dist == 'darwin':
        os.system(f'secrets-push.sh')
    elif dist == 'Kali':
        os.system(f'secrets-pull.sh')


def sort_ip(data: Iterable[str], rv_dict: bool = False, rv_ipv4: bool = False,
            rv_named: bool = False) -> Union[list[IPv4Address], list[str], list[IPv4Named], dict[str, IPv4Address]]:
    """
    Sort IPs.
    Args:
        data: data.
        rv_dict: dict rv with IPv4Address.
        rv_ipv4: list rv with IPv4Address.
        rv_named: list rv with IPv4Address and str.

    Returns:
        Union[list[IPv4Address], list[str], dict[str, IPv4Address]]:
    """
    data = iter_split(data)
    if rv_dict or rv_ipv4 or rv_named:
        rv = sorted([ipaddr(addr) for addr in iter_split(data)])
        if rv_dict or rv_named:
            rv = {item.exploded: item for item in rv}
            if rv_named:
                rv = [IPv4Named(value, key) for key, value in rv.items()]
        return rv
    return sorted(iter_split(data), key=IPv4Address)


def sub_run(command: str = None, arguments: tuple = tuple()) -> Any:
    """
    Subprocess run.

    Args:
        command: os command to run.
        arguments: os command arguments.

    Returns:
        Union[subprocess.CompletedProcess[Str], subprocess.CompletedProcess]:
    """
    try:
        return subprocess.run([command, *arguments], stdout=subprocess.PIPE, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        repr(e)


def sub_run_sys(command: str = None, arguments: tuple = tuple()) -> int:
    """
    Subprocess run with the same interpreter as the module has been invoked.

    Args:
        command: command to run.
        arguments: command arguments.

    Returns:
        int:
    """
    try:
        ret = subprocess.check_call([sys.executable, '-m', command, *arguments])
        return ret
    except subprocess.CalledProcessError as e:
        repr(e)


def tasks(count: bool = False, find: str = False, name: str = False,
          state: TasksLiteral = None) -> typing.Union[dict, str, TasksNamed]:
    ts = asyncio.all_tasks() if aioloop() else dict()
    rv = {task_state: {task.get_name(): task for task in ts if task._state == task_state.upper()}
          for task_state in TasksNamed._fields}

    if state:
        return rv.get(state, dict())
    elif count:
        return TasksNamed(*[len(rv.get(task_state, 0)) for task_state in TasksNamed._fields])
    elif find:
        return {name: task for name, task in rv[tasks_named.pending].items() if find in name}
    elif name:
        for task_state in TasksNamed._fields:
            if name in rv.get(task_state).keys():
                return task_state
    return TasksNamed(*[rv.get(task_state, dict()) for task_state in TasksNamed._fields])


def to_dict_or_list(data: Union[dict, list], name: str = None) -> Union[dict, list]:
    """
    Converts dictionaries to list and list of dicts to dicts.

    Args:
        data: data.
        name: key name for the dict key to add for list or to delete for dict.

    Returns:
        Union[dict, list]
    """
    if isinstance(data, dict):
        rv = list()
        for key, value in data.items():
            if isinstance(value, dict):
                value[name] = key
            else:
                value = {key: value}
            rv.append(value)
    else:
        rv = dict()
        for item in data:
            if isinstance(item, dict):
                if key := item.get(name):
                    del item[key]
                    rv |= {key: item}
    return rv


def trace(frame, evnt, args):
    """
    Examples:
        sys.settrace(trace)

    Args:
        frame:
        evnt:
        args:

    Returns:

    """
    frame.f_trace_opcodes = True
    stack = traceback.extract_stack(frame)
    pad = "   " * len(stack) + "|"
    if evnt == 'opcode':
        with io.StringIO() as out:
            dis.disco(frame.f_code, frame.f_lasti, file=out)
            lines = out.getvalue().split('\\n')
            [print(f"{pad}{l}") for l in lines]
    elif evnt == 'call':
        print(f"{pad}Calling {frame.f_code}")
    elif evnt == 'return':
        print(f"{pad}Returning {args}")
    elif evnt == 'line':
        print(f"{pad}Changing line to {frame.f_lineno}")
    else:
        print(f"{pad}{frame} ({evnt} - {args})")
    print(f"{pad}----------------------------------")
    return trace


def true_bool(value: Union[str, bool] = None, none_as_false: bool = True) -> Optional[bool]:
    """
    Return a bool for the arg.

    Args:
        value: value
        none_as_false: returns False if None or None.

    Returns:
        Optional[bool]:
    """
    if isinstance(value, bool):
        return value
    if value is None and not none_as_false:
        return None
    if isinstance(value, str):
        value = value.lower()
    if value in ('yes', 'on', '1', 'true', 1):
        return True
    return False


@app.command(context_settings=context)
def tty_max(stdout: bool = False) -> int:
    """
    Max tty width.

    Args:
        stdout: stdout.

    Returns:
        int:
    """
    try:
        tty_max_width = shutil.get_terminal_size().columns
    except OSError:
        tty_max_width = 80
    if stdout:
        console.print(tty_max_width)
    return tty_max_width


def upcase_values(mydict: dict, keys: list = None) -> dict:
    if keys is None:
        keys = []
    for key in keys:
        value = mydict.get(key)
        if value is not None:
            mydict[key] = value.upper()
    return mydict


def upgrade_message(p: str = str(), out: bool = False):
    """
    Prints message to user if package must be upgraded.

    Args:
        p: package.
        out: exit.
    """
    p = p if p else _path_installed.name
    upgrade, current, latest = package_info(p)
    latest = package_latest(p)
    if latest != current:
        sty.fg.orange = sty.Style(sty.RgbFg(255, 150, 50))
        print(sty.fg.orange + f'Please upgrade: {p} ({latest})' + sty.fg.rs)
        print(f'  INSTALLED: {current}')
        print(f'  LATEST:    {latest}')
        print(sty.fg.orange + f'python3 -m pip install --upgrade {p}' + sty.fg.rs)
        print()
    if out:
        sys.exit(1)


def vars_to_dict(search_dict: dict, variables: Union[str, list, dict]) -> dict:
    """
    List or string words to dict with vars and values from dict.

    Args:
        search_dict: search_dict
        variables: variables

    Returns:
        dict:
    """
    if isinstance(variables, str):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in variables.split()}
    elif isinstance(variables, list):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in variables}
    elif isinstance(variables, dict):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in list(variables)}


@app.command(context_settings=context, name='v')
def _version():
    """Version."""
    typer.echo(bapy.version)
    raise typer.Exit()


# </editor-fold>

# <editor-fold desc="IpPort">
@dataclasses.dataclass
class IpPort:
    """
    Open Ports Class.

    Examples:

    """
    down: Path = 'ips_down.txt'
    invalid: Path = 'ips_invalid.txt'
    log: LogR = _log
    open: Path = 'ips_open.json'

    @staticmethod
    def ip_port_tuple(port: Union[str, int] = 27017, ip: str = localhost) -> tuple:
        return ip, port

    @staticmethod
    async def is_global_ip(ip: str, p: Path = None) -> Optional[bool]:
        """
        Checks if Valid and Global IP.

        Args:
            ip: ip.
            p: path to save invalid IP.

        Returns:
            Optional[bool]:
        """
        try:
            ip: IPvType = await Sem.OS.sem(executor, ipaddr, ip)
            if ip.is_global:
                return True
        except ValueError:
            pass
        if p:
            p = p.touch_add(IpPort.invalid)
            p.append_text(f'{ip}\n')
        return None

    async def ping(self, ip: str, p=None) -> Optional[bool]:
        """
        Pings host.

        Args:
            ip: ip.
            p: path to save invalid IPs.

        Returns:
            Optional[bool]:
        """
        pings = 3
        rv = None
        if await self.is_global_ip(ip, p):
            cmd_out = await Sem.PING.sem(aiocmd, f'sudo ping -c {pings} {ip}')
            if cmd_out.rc == 0:
                rv = True
            elif cmd_out.rc == 2:
                rv = False
            else:
                rv = None
            if p and not rv:
                p = p.touch_add(self.down)
                p.append_text(f'{ip}\n')
        return rv

    async def is_port_proto_open(self, port: Union[str, int] = 27017, ip: str = localhost, proto: str = proto_name.tcp,
                                 status: bool = False, p: Path = None) -> Union[bool, ProtoStatus]:
        """
        Port Open.

        Args:
            port: port.
            ip: host ip.
            proto: proto.
            status: return only bool or tuple with all values.
            p: path to save invalid IPs and ip down.

        Returns:
            Union[bool, ProtoStatus]: True if open (process listing on port).
        """

        ip_port = self.ip_port_tuple(port, ip)
        if await self.ping(ip, p):
            try:
                if proto == proto_name.tcp:
                    async with Sem.SOCKET.sem(socket.socket, socket.AF_INET, socket.SOCK_STREAM) as s:
                        res = s.connect_ex(ip_port)
                        rv = not bool(res)
                else:
                    res = await Sem.NMAP.sem(aiocmd, f'nc -vnzu "{ip}" "{port}" > /dev/null 2>&1')
                    rv = not bool(res.rc)
                if status:
                    return ProtoStatus(ip, port, proto, rv)
                return rv
            except OSError as exception:
                await self.log.adebug(f'{ip=}', f'{port=}', f'{proto=}', f'{exception=}')

    async def which_open(self, ip: str = localhost, p: Path = None) -> Union[dict, list]:
        """
        Scan host or hosts.

        Args:
            ip: host or hosts.
            p: path to store json output, invalid IPs and IPs down.

        Returns:
            Union[dict, list]:
        """
        import tqdm.asyncio
        if p:
            (p / IpPort.invalid).rm()
            (p / IpPort.down).rm()

        rv = dict()
        if text := isinstance(ip, str):
            ip = list(ip)
            rv = list()

        tcp_task = tuple(self.is_port_proto_open(port, i, status=True)
                         for i in ip for port in all_ports)
        udp_task = tuple(self.is_port_proto_open(port, i, proto_name.udp, True)
                         for i in ip for port in all_ports)

        ip_status = list()
        pbar = tqdm.asyncio.tqdm()
        previous_ip = str()
        for f in pbar.as_completed(tcp_task + udp_task):
            port_status = await f
            ip_status.append(port_status)
            if port_status.ip != previous_ip:
                pbar.set_description(port_status)
                self.log.info(f'Open Completed: {port_status.ip}')
                previous_ip = port_status.ip

        for port_status in ip_status:
            ip_ports = dict()
            if port_status.tcp:
                ip_ports[proto_name.tcp] = port_status.port
            if port_status.udp:
                ip_ports[proto_name.udp] = port_status.port
            if ip_ports and text:
                rv.append(ip_ports)
            elif ip_ports and text is False:
                rv.update({port_status.ip: ip_ports})

        p = p.touch_add(IpPort.open)
        with p.open(mode='w') as f:
            f.write(json.dumps(rv, indent=4, sort_keys=True))
        return rv


# </editor-fold>

# <editor-fold desc="Mongo">
@dataclasses.dataclass
class Mongo:
    """Mongo DB Base Helper Class."""
    _db_name: str = 'test'
    _col_name: str = _db_name
    debug_async: bool = _env.debug_async.value
    host: str = '127.0.0.1'
    log: LogR = _log.child
    password: NameDefault = datafield(default_factory=NameDefault)
    port: int = None
    retry: bool = True
    srv: bool = True
    test: bool = False
    username: NameDefault = datafield(default_factory=NameDefault)
    connect_timeout = 200000
    col_test_prefix = _db_name
    FiltersBase = collections.namedtuple('FiltersBase', 'col_names')
    filters_base = FiltersBase({"name": {"$regex": r"^(?!system\.|.*file|.*glob|.*invalid)"}})
    max_pool = sum(Sem.MONGO.total.values())
    mongo_exceptions = (socket.gaierror, pymongo.errors.ConnectionFailure, pymongo.errors.AutoReconnect,
                        pymongo.errors.ServerSelectionTimeoutError, pymongo.errors.ConfigurationError,)
    server_timeout = 300000

    def __post_init__(self):
        _env.aiodebug(self.debug_async)
        env = environs.Env()
        env.read_env(Package.mongo.text)
        if self.password.name:
            self.password = password if (password := env(self.password.name, self.password.default)) else str()
        if self.username.name:
            self.username = username if (username := env(self.username.name, self.username.default)) else str()

    # noinspection PyMethodParameters
    @decorator
    def connect_try(func, self, *args, **kwargs):
        log = dict(rv=['db', 'col'], args=[], kwargs=[])
        self.log.debug(f'Start: {func.__qualname__}', f'{args=}', f'{kwargs=}')
        rv = None
        while True:
            try:
                # noinspection PyCallingNonCallable
                rv = func(self, *args, **kwargs)
                if func.__name__ in log['rv']:
                    self.log.info(f'{func.__qualname__=}', fmi(args), fmi(kwargs), fmi(rv))
                break
            except self.mongo_exceptions as exception:
                self.log.warning(f'Waiting for connection: {func.__qualname__=}, {args=}, {repr(exception)}')
                Nap.MONGO.sleep()
                continue
        self.log.debug(f'End: {func.__qualname__}', f'{args=}', f'{kwargs=}')
        return rv

    @connect_try
    def col(self, name: str = None, coro: bool = True) -> MongoCol:
        call = caller(False)
        self.log.debug('Start', f'{call.args=}', f'{call.task=}', f'{call.coro=}')
        name = name if name else self.col_name
        name = f'{self.col_test_prefix}_{name}' if self.test or Mongo._db_name not in name else name
        uri, kwargs = self.url
        func = MongoClientMotor if coro else MongoClientPy
        rv = func(uri, **kwargs).get_database(self.db_name).get_collection(name)
        self.log.debug(f'End', f'{call.args=}', f'{call.task=}', f'{call.coro=}', f'{type(rv)=}', f'{rv.name=}')
        return rv

    @property
    def col_name(self) -> str:
        return self._col_name

    @col_name.setter
    def col_name(self, value: str):
        self._col_name = value

    @property
    @memonoself
    def url(self) -> tuple[str, dict]:
        port = f':{self.port}' if self.port else str()
        retry = '?retryWrites=true&w=majority' if self.retry else str()
        srv = '+srv' if self.srv else str()
        return f'mongodb{srv}://{self.username}:{self.password}@{self.host}{port}/{self.db_name}{retry}', \
               dict(connectTimeoutMS=self.connect_timeout, serverSelectionTimeoutMS=self.server_timeout,
                    maxPoolSize=self.max_pool)

    @property
    def db_name(self) -> str:
        return self._db_name

    @db_name.setter
    def db_name(self, value: str):
        self._db_name = value

    @connect_try
    def find(self, col: str = None, find: dict = None) -> MongoCursorPy:
        return self.col(col, False).find(find if find else dict())

    async def find_one_and_update(self, _id: Any, value: MongoFieldValue, col: str = None):
        return await self.col(col).find_one_and_update({'_id': _id}, {'$set': value}, upsert=True)


# </editor-fold>

# <editor-fold desc="Nmap">
class NmapProtoEnum(EnumDict):
    IP = 'P'
    SCTP = 'S'
    TCP = 'T'
    UDP = 'U'


class NmapStateEnum(EnumDict):
    CLOSED = EnumDict.auto()
    FILTERED = EnumDict.auto()
    OPEN = EnumDict.auto()


@dataclasses.dataclass
class NmapParse(AsDict):
    args: str = str()
    debugging: dict = datafield(default_factory=dict)
    host: Union[dict, list] = datafield(default_factory=dict)
    ip: str = str()
    name: EnumDictType = None
    nmaprun: dict = datafield(default_factory=dict)
    rc: int = int()
    runstats: dict = datafield(default_factory=dict)
    scaninfo: dict = datafield(default_factory=dict)
    scanner: str = str()
    stderr: Union[str, list] = str()
    start: str = str()
    startstr: str = str()
    verbose: dict = datafield(default_factory=dict)
    version: str = str()
    xmloutputversion: str = str()
    elapsed: str = datafield(default=str(), init=False)
    extraports: list[dict] = datafield(default_factory=list, init=False)
    os: dict = datafield(default_factory=dict, init=False)
    port: list[dict] = datafield(default_factory=list, init=False)
    ports: dict = datafield(default_factory=dict, init=False)

    def __post_init__(self):
        elapsed = dpath.util.get(self.nmaprun, '/runstats/finished/elapsed', default=str())
        self.elapsed = str(datetime.timedelta(seconds=int(elapsed.split('.')[0]))).split('.')[0]
        self.os = self.host.get('os', dict())
        self.ports = self.host.get('ports', dict())
        extraports = self.ports.get('extraports', list())
        self.extraports = [extraports] if isinstance(extraports, dict) else extraports
        port = self.ports.get('port', list())
        self.port = [port] if isinstance(port, dict) else port

    @classmethod
    def parse(cls, **kwargs):
        return cls(**kwargs | kwargs.get('nmaprun'))


@dataclasses.dataclass
class NmapProto(AsDict):
    ip: Any
    sctp: Any
    tcp: Any
    udp: Any


@dataclasses.dataclass
class NmapState(AsDict):
    closed: Any
    filtered: Any
    open = Any


@dataclasses.dataclass
class NmapServiceScript(AsDict):
    name: Union[list, str]
    value: dict


@dataclasses.dataclass
class NmapPort(AsDict):
    number: int
    state: NmapStateEnum
    proto: NmapProtoEnum
    script: Optional[NmapServiceScript] = None
    service: Optional[NmapServiceScript] = None


@dataclasses.dataclass
class NmapCodec(AsDict):
    parsed: dict[str, dict]


@dataclasses.dataclass
class NmapCommand(AsDict):
    _command: str = datafield(default=str(), init=False)
    _ip: Optional[IPvType] = None
    debug_async: bool = _env.debug_async.value
    hostname: tuple = 'kali', 'scan'
    log: LogR = _log
    name: EnumDictType = None
    os: bool = False
    parse: NmapParse = datafield(default=None, init=False)
    pn: bool = True
    _port: NmapCommandPortTyping = str()
    samples: dict = datafield(default_factory=dict)
    script: NmapCommandScriptTyping = str()
    script_args: str = str()
    ss: bool = True
    su: bool = True
    sv: bool = False
    sy: bool = True
    sz: bool = True
    t: Optional[int] = None

    def __post_init__(self):
        self.install()
        self.command()

    def command(self, ip: IPAddressLike = None, port: NmapCommandPortTyping = None):
        self.ip = ip if ip else self.ip
        self.port = port if port else self.port

        _script = dict(category=['auth', 'broadcast', 'default', 'discovery', 'dos', 'exploit', 'external', 'fuzzer',
                                 'intrusive', 'malware', 'safe', 'version', 'vuln'],
                       exclude=['broadcast-*', 'ipv6-*', 'targets-ipv6-*', 'lltd-discovery', 'dns-brute',
                                'hostmap-robtex', 'http-robtex-shared-ns', 'targets-asn', 'hostmap-crtsh',
                                'http-icloud-*', 'http-virustotal', 'eap-info'],
                       args=['newtargets'], )
        script = f'({" or ".join(_script["category"])}) and not {" and not ".join(_script["exclude"])}' \
            if self.script == 'complete' else self.script
        script_args = ",".join(_script["args"]) \
            if self.script == 'complete' else self.script_args
        p = f' {self.port}' if self.port and self.port != '-' else self.port
        self._command = f'sudo nmap -R -r --reason -oX - ' \
                        f'{"-O --osscan-guess " if self.os else str()}' \
                        f'{f"-p{p} " if self.port else str()}' \
                        f'{"-Pn " if self.pn else str()}' \
                        f'{f"-script {script} " if script else str()}' \
                        f'{f"-script-args {script_args} " if script_args else str()}' \
                        f'{"-sS " if self.ss else str()}' \
                        f'{"-sU " if self.su else str()}' \
                        f'{"-sV --version-all " if self.sv else str()}' \
                        f'{"-sY " if self.sy else str()}' \
                        f'{"-sZ " if self.sz else str()}' \
                        f'-T{self.t if self.t else 4 if Machine.hostname in self.hostname else 3} ' \
                        f'{f"-{self.ip.version}" if self.ip else str()}' \
                        f'{self.ip.exploded} ' \
                        f'| grep -v "Fetchfile found "'
        return self._command

    @staticmethod
    @once
    def install():
        Distro.install('nmap')

    @property
    def ip(self) -> Optional[IPvType]:
        return self._ip

    @ip.setter
    def ip(self, value: Optional[IPAddressLike]):
        if value:
            self._ip = ipaddr(value)
        else:
            self._ip = value

    @property
    def port(self) -> Union[str, int]:
        return self._port

    @port.setter
    def port(self, value: Union[str, int]):
        self._port = value

    async def run(self, ip: str = str(), name: EnumDictType = None, port: NmapCommandPortTyping = None) -> NmapParse:
        self.ip = ip if ip else self.ip
        self.name = name if name else self.name

        if self.samples:
            cmd_out = CmdOut(str(), str(), int())
            nmaprun = self.samples[name].get(self.ip, dict())
        else:
            cmd_out = await aiocmd(self.command(port=port), utf8=True)
            try:
                nmaprun = xmltodict.parse(cmd_out.stdout, dict_constructor=dict,
                                          process_namespaces=True, attr_prefix='')['nmaprun']
            except xml.parsers.expat.ExpatError as exception:
                nmaprun = dict()
                cmd_out = CmdOut(str(), f'{exception=}, {self.command=}, {self.ip=}', 255)
                await self.log.aerror(f'{exception=}', f'{cmd_out.stdout=}', f'{self.command=}', f'{self.ip=}')

        self.parse = NmapParse.parse(ip=self.ip, name=self.name, nmaprun=nmaprun, rc=cmd_out.rc, stderr=cmd_out.stderr)
        return self.parse


# </editor-fold>


__all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]

if __name__ == '__main__':
    bapy.env.aiodebug()
    try:
        typer.Exit(app())
    except KeyboardInterrupt:
        red('Aborted!')
        typer.Exit()
