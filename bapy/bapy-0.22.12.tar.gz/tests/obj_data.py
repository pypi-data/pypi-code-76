#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dataclasses
import inspect
from typing import NamedTuple

import environs

from bapy import AsDict
from bapy import _log
from bapy import LogR
from bapy import Obj
from bapy import Path

Named = NamedTuple('Named', a=str)
named = Named('a')
obj_named = Obj(named)

obj_str = Obj('__s__')


class AsDictTestA(AsDict):
    _a = 1
    c = 3
    log = _log

    __exclude_attr__ = ['b', ]

    def __init__(self):
        # self.env = environs.Env()
        self._b = 2
        self._d = 4

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b


obj_AsDictTestA = Obj(AsDictTestA)

asdict_test_a = AsDictTestA()
obj_asdict_test_a_prop_ = Obj(asdict_test_a, prop=True, swith='_')


class AsDictTestB(AsDict):
    _a = 1
    asdict_test_a = asdict_test_a
    env = environs.Env()
    path = Path()


obj_AsDictTestB = Obj(AsDictTestB)

asdict_test_b = AsDictTestB()
obj_asdict_test_b = Obj(asdict_test_b)


@dataclasses.dataclass
class AsDictDataTestA(AsDict):
    a: str = 'a'
    log: LogR = _log
    asdict_test: AsDictTestA = asdict_test_a
    env: environs.Env = environs.Env()
    path: Path = Path()


obj_AsDictDataTestA = Obj(AsDictDataTestA)

asdict_data_test_a = AsDictDataTestA()
obj_asdict_data_test_a = Obj(asdict_data_test_a)


@dataclasses.dataclass
class AsDictDataTestB(AsDict):
    asdict_data_test_a: AsDictDataTestA = asdict_data_test_a


obj_AsDictDataTestB = Obj(AsDictDataTestB)

asdict_data_test_b = AsDictDataTestB()
obj_asdict_data_test_b = Obj(asdict_data_test_b)

__all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]
