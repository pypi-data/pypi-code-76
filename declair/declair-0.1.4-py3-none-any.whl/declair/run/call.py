"""
Functions that simplify calling functions and types from dictionaries.
"""
# TODO: Make __call__'s args such a key that the list which is its
#       value is not split up into sub-entries by default. This would be very
#       convenient as it would not require writing the {__tuple__: [...]}
#       wrapper in most cases which don't require it. One way to implement it
#       would be to ignore args for search by default, unless all of
#       the elements of the list are __tuple__ tuples. This would work on the
#       basis that args must always receive a tuple/list, and the code
#       could just automatically choose the thing which is not broken.

from ..exception import InvalidConfigException
from ..serialization import string_to_type

from .insertion import make_insert_func_recursive

from .special_entries import CALL_KEY

CALL_ARGS_KEY = 'args'
CALL_KWARGS_KEY = 'kwargs'

def _call_dict(obj):
    if type(obj[CALL_KEY]) == str:
        call_func = string_to_type(obj[CALL_KEY])
    else:
        call_func = obj[CALL_KEY]
    call_args = [insert_call_results(x) for x in obj.get(CALL_ARGS_KEY, ())]
    call_kwargs = {key: insert_call_results(x)
                   for key, x in obj.get(CALL_KWARGS_KEY, {}).items()}
    return call_func(*call_args, **call_kwargs)

@make_insert_func_recursive(CALL_KEY)
def insert_call_results(obj):
    """
    Inserts results of calling all execution time dictionaries of form
    {
        "__call__": <function or type string>,
        "args": <args list> (optional),
        "kwargs": <kwargs dict> (optional)
    }
    """
    try:
        return _call_dict(obj)
    except:
        raise InvalidConfigException("Failed to call dictionary: {}".format(
                    obj))
