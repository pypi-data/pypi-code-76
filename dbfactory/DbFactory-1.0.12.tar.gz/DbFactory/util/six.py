# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:    six.py
   Description:  单例模式
   Author:       Caturbhuja
   date:         2020/8/31
   WeChat:       chending2012
-------------------------------------------------
   Change Activity:
       2020/8/31:   DB工厂类创建

-------------------------------------------------
"""
__author__ = 'Caturbhuja'

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    def iteritems(d, **kw):
        return iter(d.items(**kw))
else:
    def iteritems(d, **kw):
        return d.iteritems(**kw)


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class MetaClass(meta):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    # 直接指定 bases 为空，忽略 MixinFunction ，实现 MixinFunction 作为IDLE提示
    return type.__new__(MetaClass, 'caturbhuja_das', (), {})
