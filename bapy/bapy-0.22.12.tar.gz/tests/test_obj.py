#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections
import inspect
from typing import Callable

from bapy import ic
from obj_data import *


def test_obj_get():
    assert obj_AsDictTestA.get_class == obj_asdict_test_a_prop_.get_class
    assert obj_AsDictTestA.get_class == obj_asdict_test_a_prop_.get_class
    assert obj_asdict_test_b.get_mro == (obj_asdict_test_b.get_class, Obj(AsDict).get_class, type(object()))
    assert obj_asdict_test_a_prop_.get_mro_asdict_exclude == sorted(
        set(list(obj_asdict_test_b.get_mro_asdict_exclude) + list(AsDictTestA.__asdict_exclude__)))
    for item in obj_asdict_test_a_prop_.get_mro_class_exclude:
        assert item in obj_asdict_test_a_prop_.__exclude_copy__
    assert obj_str.get_module == inspect.getmodule('__s__')


def test_obj_has():
    pass


def test_obj_is():
    assert Obj(True).is_bool
    assert Obj(b'a').is_bytes
    assert Obj(test_obj_is).is_callable
    assert Obj(Obj).is_class
    assert obj_AsDictDataTestA.is_dataclass
    assert not obj_asdict_data_test_a.is_dataclass
    assert not obj_AsDictDataTestA.is_dataclass_instance
    assert obj_asdict_data_test_a.is_dataclass_instance
    assert Obj(collections.defaultdict()).is_defaultdict
    assert Obj({}).is_dict
    assert Obj({}).is_dlst
    assert Obj(list()).is_dlst
    assert Obj(set()).is_dlst
    assert Obj(tuple()).is_dlst
    assert obj_str.is_end
    assert obj_str.asdict_excluded
    assert Obj(collections).asdict_excluded
    assert Obj(test_obj_is).asdict_excluded
    assert Obj(Obj).asdict_excluded
    assert Obj(Callable).asdict_excluded
    assert Obj(1.1).is_float
    assert Obj(1).is_int
    assert obj_str.is_iterable
    assert Obj(list()).is_lst
    assert Obj(set()).is_lst
    assert Obj(tuple()).is_lst
    assert not Obj(dict()).is_lst
    assert Obj(list()).is_mlst
    assert Obj(set()).is_mlst
    assert Obj(tuple()).is_mlst
    assert Obj(dict()).is_mlst
    assert not Obj(1).is_mlst
    assert Obj(dict()).is_mlst
    assert Obj(collections).is_module
    assert Obj(collections.UserDict({})).is_mutablemapping
    assert obj_named.is_namedtuple
    assert not obj_named.is_obj_dict
    assert obj_asdict_data_test_a.is_obj_dict
    assert not obj_AsDictTestB.is_obj_dict
    assert obj_asdict_test_b.is_obj_dict
    assert Obj(collections.OrderedDict({})).is_ordereddict
    assert Obj(test_obj_is).is_routine
    assert Obj(set()).is_set
    assert not Obj(test_obj_is).is_set
    assert obj_str.is_start
    assert Obj('_s__', swith='_').is_start
    assert obj_str.is_str
    assert not obj_str.is_tuple
    assert obj_named.is_tuple
    ic(obj_asdict_test_a_prop_.get_mro_asdict_exclude)


ic(obj_AsDictTestA.get_class)
ic(obj_asdict_test_a_prop_.get_class)
ic(obj_asdict_test_b.get_mro)
ic(obj_asdict_test_a_prop_.get_mro_asdict_exclude)
ic(sorted(set(list(obj_asdict_test_b.get_mro_asdict_exclude) + list(AsDictTestA.__asdict_exclude__))))

