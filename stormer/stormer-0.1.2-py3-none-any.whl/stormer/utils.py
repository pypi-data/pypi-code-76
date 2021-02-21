#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created By Murray(murray) on 2021/1/28 上午10:39
--------------------------------------------------
"""
import uuid


def val_of(data, idx, default=None, typ=None, is_hex=False):
    try:
        if isinstance(data, (str, int, float, bytes, uuid.UUID)):
            val = data
        elif isinstance(data, (list, dict, tuple)):
            val = data[idx]
        else:
            val = getattr(data, idx, default)
        if typ is not None:
            if typ in [int, float]:
                val = typ(val or 0)
            elif is_hex and isinstance(val, uuid.UUID):
                val = val.hex
            if val is not None:
                val = typ(val)
    except (Exception,):
        val = None
    val = default if val is None else val
    return val
