from typing import List, Optional


def generate_key(
    *, key, args, kwargs, kwargs_list: Optional[List] = None,
    check_params: bool = False, check_args_params: bool = False,
    check_kwargs_params: bool = False
):
    kwargs_name = kwargs
    tail = ''
    if kwargs_list:
        kwargs_name = {kw: kwargs.get(kw) for kw in kwargs_list}
    if check_params or (check_args_params and check_kwargs_params):
        tail = f'-{args}-{kwargs_name}'
    elif check_args_params and check_kwargs_params is False:
        tail = f'-{args}'
    elif check_kwargs_params and check_args_params is False:
        tail = f'-{kwargs_name}'
    return f'{key}{tail}'
