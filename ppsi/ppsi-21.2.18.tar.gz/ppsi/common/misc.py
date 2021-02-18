#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020-2021 Pradyumna Paranjape
# This file is part of ppsi.
#
# ppsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ppsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ppsi.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Miscellaneous functions and constants for ppsi/pspbar
'''


import typing
from collections import Iterable


def subdict2dict(*subs: dict) -> dict:
    '''
    Convert a list of dictionaries to single dictionary.

    Args:
        *sub: dict [inside an iterable such as list]

    Returns:
        dict of all ``sub`` compiled together
    '''
    key_val_dict = {}
    for sub in subs:
        for key_item, val_item in sub.items():
            key_val_dict[key_item] = val_item
    return key_val_dict


def key2dict(keys: typing.Iterable,
             vals: typing.Union[object, typing.Iterable] = None,
             pairwise: bool = False) -> dict:
    '''
    Convert List of keys [and of values] to a dictionary.

    Args:
        keys: to be converted to dict
        vals: default value to be imparted to every key
            CAUTION: same 'reference' is passed, changing one will change all
        pairwise:
             ``*keys`` -> ``*vals`` pairwise association
            ``vals`` must be iterable, ``len(keys) == len(vals)``

    Raises:
        ValueError: ``keys`` and ``vals`` length mismatches

    Returns:
        Dict[keys, vals]
    '''
    if isinstance(keys, dict):
        return keys
    if all(isinstance(sub, dict) for sub in keys):
        return subdict2dict(*list(keys))
    keys = list(keys)
    key_val_dict = {}
    if pairwise:
        if not isinstance(keys, Iterable):
            raise ValueError("keys not iterable")
        vals = list(vals)
        if len(keys) != len(vals):
            raise ValueError("lengths of keys and vals don't match")
    else:
        vals = [vals] * len(keys)
    for key_item, val_item in zip(keys, vals):
        print(key_item)
        key_val_dict[key_item] = val_item
    return key_val_dict


def val2dict(vals: typing.Iterable,
             keys: typing.Union[object, typing.Iterable] = None,
             pairwise: bool = False) -> dict:
    '''
    Convert List of values [and of keys] to a dictionary.

    Args:
        vals: to be converted to dict
        keys: default key that refers ``vals``
        pairwise:
            ``*keys`` -> ``*vals`` pairwise association
            ``keys`` must be iterable, ``len(keys) == len(vals)``

    Raises:
        KeyError: ``keys`` and ``vals`` length mismatches

    Returns:
        Dict[keys, vals]
    '''
    if isinstance(keys, dict):
        return keys
    if all(isinstance(sub, dict) for sub in vals):
        return subdict2dict(*list(vals))
    vals = list(vals)
    if not pairwise:
        return {keys: vals}
    if not isinstance(keys, Iterable):
        raise KeyError("keys not iterable")
    keys = list(keys)
    if len(keys) != len(list(vals)):
        raise KeyError("lengths of keys and vals don't match")
    key_val_dict = {}
    for key_item, val_item in zip(keys, vals):
        key_val_dict[key_item] = val_item
    return key_val_dict


def iter2dict(in_iter: typing.Iterable, iter_type: str = 'keys',
              in_pair: typing.Union[object, typing.Iterable] = None,
              pairwise: bool = False) -> dict:
    '''
    Convert a list of iterables [and pairs] to dictionary.

    Args:
        in_iter: to be converted to dict
        iter_type: interpret elements as [keys, vals]
        in_pair: to be paired with in_iter
        pairwise:
            ``*in_iter`` <-> ``*in_pair`` pairwise association
            ``in_pair`` must be iterable
            ``len(in_pair) == len(in_iter)``

    Raises:
        KeyError: <in_pair> and <in_iter> length mismatches if iter_type=keys
        ValueError: <in_pair> and <in_iter> length mismatches if iter_type=vals

    Returns:
        Dict[in_pair, in_iter]
    '''
    if iter_type == 'vals':
        return val2dict(vals=in_iter, keys=in_pair, pairwise=pairwise)
    return key2dict(keys=in_iter, vals=in_pair, pairwise=pairwise)
