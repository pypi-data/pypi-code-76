from typing import Type
import inspect

def dictionize(data) -> dict:
    if data is None:
        return {}

    output = vars(data)
    for key, value in output.items():
        if hasattr(value, '__dict__'):
            output[key] = dictionize(value)
    output = {
        key: value
        for key, value
        in output.items()
        if value is not None
    }
    return output


def undictionize(data: dict, class_: Type):
    if data is None:
        return None

    obj = class_.__new__(class_)
    for key, value in data.items():
        if isinstance(value, dict):
            value = undictionize(value, class_)
        setattr(obj, key, value)

    varnames = class_.__init__.__code__.co_varnames
    init_args = [
        data.get(varname, None)
        for varname
        in varnames
        if varname != 'self'
    ]
    obj.__init__(*init_args)
    
    # members = inspect.getmembers(obj)

    return obj
