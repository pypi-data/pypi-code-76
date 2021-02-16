"""
This module contains user-side helper functions which assist in writing
experiment code.
"""
from copy import copy

from .exception import InvalidConfigException, HelperException

def call(call_dict, *args, default_params={}):
    """Helper function for executing a manual call dictionary. Positional 
    arguments can be given after `call_dict`.

    A manual call dictionary is a dictionary of form
    {
        "call": <function>
        "params": <parameters>
    }
    where we wish to execute <function> with arguments <parameters>.

    If "params" is not given, it is taken to be `default_params`.

    Any key from `default_params` not in "params" is taken to be its
    corresponding value from `default_params`.
    """
    if 'call' not in call_dict:
        raise InvalidConfigException("The dictionary does not contain a 'call' key")
    if 'params' not in call_dict:
        params = default_params
    else:
        params = copy(call_dict['params'])
        for key, value in default_params.items():
            if key not in params:
                params[key] = value
    try:
        return call_dict['call'](*args, **params)
    except:
        raise HelperException('Failed to call {} with args {} and kwargs {}'.format(call_dict['call'], args, params))
