"""
Functions for searching in sources.
"""
import inspect
from os.path import abspath, dirname

from .special_entries import ENTRIES_WITH_SOURCES
from .insertion import make_insert_func_recursive
from ..serialization import string_to_type

def _does_this_dict_contain_sources(obj):
    return any(entry in obj for entry in ENTRIES_WITH_SOURCES)

def _get_source_of_type_string(type_string):
    # Here we find the source file of a type/function/object/thing, which is
    # easiest to do by just importing it and inspecting
    instance = string_to_type(type_string)
    return inspect.getfile(instance)

def find_sources(obj):
    sources = set()
    @make_insert_func_recursive(_does_this_dict_contain_sources)
    def retrieve_sources(dict_):
        for key, value in dict_.items():
            if key in ENTRIES_WITH_SOURCES:
                # we need try-except in case e.g. builtins, like math.cos, are
                # put in
                try:
                    sources.add(_get_source_of_type_string(value))
                except TypeError:
                    pass
            if (isinstance(value, list) 
                    or isinstance(value, tuple)
                    or isinstance(value, dict)):
                find_sources(value)
    retrieve_sources(obj)
    return sources
