import numpy as np
import torch
import random


def set_core_seed(seed):
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def registry_func(name: str, decorators=None, save_dict=dict()):
    def actual_func(obj):
        save_dict[name] = obj if decorators is None else decorators(obj)
        return obj

    return actual_func


def pop_first_non_none_value(*args, msg="default error msg"):
    for arg in args:
        if arg is not None:
            return arg
    raise f"{msg} can't find non-none value"


def parser_process_function(process_func_str):
    import pyparsing as pp

    _func_name = pp.Word(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/_"
    )
    _var = pp.Word(
        "!\"#$%&'*+-./0123456789:;<>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    )
    _kwarg = _var + pp.Literal("=") + _var
    _func = pp.Forward()
    _func <<= _func_name + (
        pp.Literal("(")
        + pp.Optional(pp.delimitedList(_kwarg | _var | "''" | '""'), "")
        + pp.Literal(")")
    )
    parse_result = _func.parseString(process_func_str)
    assert parse_result[1] == "(" and parse_result[-1] == ")"
    parse_length = len(parse_result)
    parse_result = list(parse_result)
    function = parse_result[0]
    args_index = parse_length if "=" not in parse_result else parse_result.index("=")
    args = parse_result[2 : args_index - 1]
    kwargs_index = [i for i in range(2, parse_length - 1) if parse_result[i] == "="]
    kwargs = dict({parse_result[i - 1]: parse_result[i + 1] for i in kwargs_index})
    ret = dict({"function": function, "args": args, "kwargs": kwargs})
    return ret
