from functools import wraps
from pydantic import BaseModel
import inspect
from magicapi import g

from magicapi.Decorators.helpers import async_safe


def parse_objects(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        sigs = inspect.signature(f)
        parameters = sigs.parameters
        args = list(args)
        for i, (arg, param) in enumerate(zip(args.copy(), parameters.values())):
            this_class = param.annotation
            if inspect.isclass(this_class) and issubclass(param.annotation, BaseModel):
                args[i] = this_class.parse_obj(arg)

        for var_name, var_val in kwargs.copy().items():
            this_class = parameters.get(var_name).annotation

            if (
                var_name in parameters
                and inspect.isclass(this_class)
                and issubclass(this_class, BaseModel)
            ):
                if var_val is not None:
                    kwargs[var_name] = this_class.parse_obj(var_val)
                else:
                    kwargs[var_name] = None

        if g.settings.print_level > 1:
            print("PARSE OBJS", "args", args, "kwargs", kwargs)

        return await async_safe(f, *args, **kwargs)

    return wrapper
