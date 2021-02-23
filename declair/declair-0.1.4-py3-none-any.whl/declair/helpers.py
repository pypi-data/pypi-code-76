"""
This module contains user-side helper functions which assist in writing
experiment code.
"""
from copy import copy

from .serialization import string_to_type
from .exception import HelperException

def manual(call_dict, *args, default_kwargs={}):
    """Helper function for executing a manual call dictionary. Basically, it's
    just for ergonomics when dealing with dictionaries of callables and
    parameters. Positional arguments of the executed function can be given
    after `call_dict`.

    A manual call dictionary is a dictionary of form
    {
        "manual": <function>,
        "args": <arguments>,
        "kwargs": <keyword arguments>
    }
    where we wish to execute <function> with positional arguments <args> and
    keyword arguments <kwargs>. Arguments given to `manual` in the `*args`
    section are appended to the list <args> given in the call dictionary.

    <function> in the dictionary can be either a callable type or a type
    string, which can be imported as a callable type.

    If `kwargs` does not contain a parameter from `default_kwargs`, it is added
    to it.
    """
    if 'manual' not in call_dict:
        raise ValueError("The manual call dictionary does not contain a 'manual' key")
    else:
        m = call_dict['manual']
        if callable(m):
            call_func = m
        elif isinstance(m, str):
            try:
                call_func = string_to_type(m)
            except:
                raise ValueError("Could not import type {}".format(m))
        else:
            raise ValueError("{} is not a callable type nor a string".format(m))
    if 'kwargs' not in call_dict:
        kwargs = default_kwargs
    else:
        kwargs = copy(call_dict['kwargs'])
        for key, value in default_kwargs.items():
            if key not in kwargs:
                kwargs[key] = value
    args_list = call_dict.get('args', []) + list(args)
    try:
        return call_func(*args_list, **kwargs)
    except:
        raise HelperException('Failed to call {} with args {} and kwargs {}'.format(call_dict['manual'], args_list, kwargs))
