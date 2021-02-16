"""
Functions for serializing and deserializing experiment config files.
"""
from importlib import import_module
import json
import os
from tempfile import gettempdir
import yaml
import re

_DEFAULT_INDENT = 4

# Fix incorrect scientific notation parsing in the YAML safe loader
# taken from https://stackoverflow.com/a/30462009
yaml_safe_loader = yaml.SafeLoader
yaml_safe_loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))


def type_to_string(type_):
    """Returns a string representation of a type, like a class or function.
    This results in a string of the form `module.type` like that normally used
    when importing code within Python.
    """
    return "{}.{}".format(type_.__module__, type_.__name__)

def string_to_type(str_):
    """Inverse operation of `type_to_string`. Imports a given type from a
    string.
    """
    split_point = len(str_) - str_[::-1].index('.')
    module_str = str_[:split_point - 1]
    attr_str = str_[split_point:]
    return getattr(import_module(module_str), attr_str)

def type_to_dict(type_):
    """Returns a dictionary containing the stringified type, which can then be
    turned into JSON."""
    type_string = type_to_string(type_)
    dict_ = {'__type__': type_string}
    return dict_

def dict_to_type(dict_):
    """Parses a dictionary with stringified type information of an object.
    Inverse operation of `type_to_dict`."""
    return string_to_type(dict_['__type__'])

class TypeEncoder(json.JSONEncoder):
    """A JSON encoder which encodes objects by their type."""
    def default(self, obj):
        try:
            return type_to_dict(obj)
        except:
            return json.JSONEncoder.default(self, obj)

def serialize_type_dict(dict_, indent=None):
    """Returns a JSON encoding of a dictionary with functions and types as
    values.

    Args:
        indent: If None, do not use any indentation. If True, use 4-space
                indentation. If a nonnegative integer n, use n-space
                indentation.
    """
    if isinstance(indent, bool) and indent is True:
        indent = _DEFAULT_INDENT
    return json.dumps(dict_, cls=TypeEncoder, indent=indent, sort_keys=True)

def load_file(path):
    with open(path) as file_:
        dict_ = yaml.load(file_, Loader=yaml_safe_loader)
    return dict_

def save_file(path, config):
    with open(path, 'w') as file_:
        file_.write(serialize_type_dict(config))
