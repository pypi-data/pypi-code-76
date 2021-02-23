from ..serialization import dict_to_type

from .insertion import make_insert_func_recursive

from .special_entries import TYPE_KEY

@make_insert_func_recursive(TYPE_KEY)
def insert_type(obj):
    return dict_to_type(obj)
