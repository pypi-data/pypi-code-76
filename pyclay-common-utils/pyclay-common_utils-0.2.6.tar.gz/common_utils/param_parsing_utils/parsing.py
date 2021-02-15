from .str_conversion import *
from ..path_utils import rel_to_abs_path

def check_required(text_str: str, required: bool, name: str):
    if required and text_str is None:
        logger.error(f"{name} is required")
        raise Exception

def none_conversion(text_str: str):
    if type(text_str) is str:
        return text_str if text_str.lower() not in ['none'] else None
    else:
        return text_str

def parse_str(text_str: str, default: str=None, required: bool=False, name='param') -> str:
    check_required(text_str, required=required, name=name)
    text_str = none_conversion(text_str)
    default = none_conversion(default)
    return text_str if text_str is not None else default

def parse_path(text_str: str, default: str=None, required: bool=False, name='param') -> str:
    check_required(text_str, required=required, name=name)
    text_str = none_conversion(text_str)
    default = none_conversion(default)
    text_str = rel_to_abs_path(text_str) if text_str is not None else None
    default = rel_to_abs_path(default) if default is not None else None
    return text_str if text_str is not None else default

def parse_bool(text_str: str, default: bool=None, required: bool=False, name='param') -> bool:
    check_required(text_str, required=required, name=name)
    text_str = none_conversion(text_str)
    default = none_conversion(default)
    return str2bool(text_str) if text_str is not None else default

def parse_int(text_str: str, default: int=None, required: bool=False, name='param') -> int:
    check_required(text_str, required=required, name=name)
    text_str = none_conversion(text_str)
    default = none_conversion(default)
    return str2int(text_str) if text_str is not None else default

def parse_float(text_str: str, default: float=None, required: bool=False, name='param') -> float:
    check_required(text_str, required=required, name=name)
    text_str = none_conversion(text_str)
    default = none_conversion(default)
    return str2float(text_str) if text_str is not None else default

def parse_strlistlist(list_str: str, default: list=None, required: bool=False, name='param') -> list:
    check_required(list_str, required=required, name=name)
    list_str = none_conversion(list_str)
    default = none_conversion(default)
    return str2strlistlist(list_str) if list_str is not None else default

def parse_intlistlist(text: str, default: list=None, required: bool=False, name='param') -> list:
    check_required(text, required=required, name=name)
    text = none_conversion(text)
    default = none_conversion(default)
    return str2intlistlist(text) if text is not None else default

def parse_floatlistlist(text: str, default: list=None, required: bool=False, name='param') -> list:
    check_required(text, required=required, name=name)
    text = none_conversion(text)
    default = none_conversion(default)
    return str2floatlistlist(text) if text is not None else default

def parse_boollistlist(text: str, default: list=None, required: bool=False, name='param') -> list:
    check_required(text, required=required, name=name)
    text = none_conversion(text)
    default = none_conversion(default)
    return str2boollistlist(text) if text is not None else default

def parse_strlist(list_str: str, default: list=None, required: bool=False, name='param') -> list:
    check_required(list_str, required=required, name=name)
    list_str = none_conversion(list_str)
    default = none_conversion(default)
    return str2strlist(list_str) if list_str is not None else default

def parse_intlist(list_str: str, default: list=None, required: bool=False, name='param') -> list:
    check_required(list_str, required=required, name=name)
    list_str = none_conversion(list_str)
    default = none_conversion(default)
    return str2intlist(list_str) if list_str is not None else default

def parse_floatlist(list_str: str, default: list=None, required: bool=False, name='param') -> list:
    check_required(list_str, required=required, name=name)
    list_str = none_conversion(list_str)
    default = none_conversion(default)
    return str2floatlist(list_str) if list_str is not None else default