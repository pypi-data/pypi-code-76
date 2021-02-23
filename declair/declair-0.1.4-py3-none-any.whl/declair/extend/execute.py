"""
This module implements experiment definition inheritance. That is, it allows an
experiment definition to expand upon some other experiment definition.
"""
from pathlib import Path

from ..const import (DEF_KEY_EXTEND_PARENT,
                     DEF_TYPE_RUN, DEF_TYPE_SEARCH, DEF_TYPE_EXTEND)
from ..exception import InvalidConfigException
from .insertion import _extend_from_file


# final_execute_func is used to avoid a circular import
def execute_extend(dict_, env, final_execute_func, filepath):
    if DEF_KEY_EXTEND_PARENT not in dict_:
        raise InvalidConfigException(
            "Definition has no valid 'extend_from' entry but is 'extend' mode.")
    if isinstance(filepath, Path):
        filepath = str(filepath)
    extended_dict = _extend_from_file(dict_, dict_[DEF_KEY_EXTEND_PARENT],
                                      filepath)
    return final_execute_func(extended_dict, env)
