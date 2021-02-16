"""Log decorator, part of the neatlog package

LICENSE
   MIT (https://mit-license.org/)

COPYRIGHT
   © 2021 Steffen Brinkmann <s-b@mailbox.org>
"""


import functools
import inspect
import logging
from pathlib import PurePath
import time
import timeit


def log(_func=None, *, level=logging.DEBUG):
    class Log:
        def __init__(self, func, *, level=level):
            functools.update_wrapper(self, func)
            self.call_count = 0
            self.func = func
            self.func_name = self.func.__name__
            self.func_filepath = inspect.getfile(self.func)
            self.func_filename = PurePath(self.func_filepath).name
            self.func_lineno = inspect.getsourcelines(self.func)[1]
            self.level = level

        def __call__(self, *args, **kwargs):
            t0 = timeit.default_timer()
            pt0 = time.process_time()
            self.call_count += 1
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            value = self.func(*args, **kwargs)
            logging.log(
                self.level,
                f"call {self.call_count} of {self.func_name}({signature}) returned {value!r};"
                f" ({(timeit.default_timer() - t0) * 1000:.3f} ms / {(time.process_time() - pt0) * 1000:.3f} ms)",
                extra={
                    "_funcName": self.func_name,
                    "_filename": self.func_filename,
                    "_lineno": self.func_lineno,
                },
            )
            return value

    if _func:
        if type(_func) is int:
            return functools.partial(Log, level=_func)
        return Log(_func)

    return Log
