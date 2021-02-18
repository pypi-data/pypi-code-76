# OPBOT - pure python3 IRC bot (bin/clean)
#
# This file is placed in the Public Domain.

"introspection"

# imports

import inspect

from .obj import Object, Ol

# functions

def find_cmds(mod):
    cmds = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                cmds[key] = o
    return cmds

def find_funcs(mod):
    funcs = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                funcs[key] = "%s.%s" % (o.__module__, o.__name__)
    return funcs

def find_mods(mod):
    mods = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                mods[key] = o.__module__
    return mods

def find_classes(mod):
    nms = Ol()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            nms.append(o.__name__, t)
    return nms

def find_class(mod):
    mds = Ol()
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            mds.append(o.__name__, o.__module__)
    return mds

def find_names(mod):
    tps = Ol()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            tps.append(o.__name__.lower(), t)
    return tps
