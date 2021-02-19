from .magic import line_magic, arg
from ..kernel_logger import logger

import re


@arg('names', nargs='*', help="variable names")
@line_magic
def tohost_magic(kernel, args):
    """Copy variables from the microcontroller to the host
Only works for variables that can be encoded in json.

Example:
    a = 'Hello from microcontroller'
    b = 123
    %tohost a b
    %%host
    print(a, b)
"""
    class Output:
        def __init__(self):
            self._ans = ''
            self._err = ''

        def fmt(self, value):
            if not value: return
            if isinstance(value, bytes): value = value.decode()
            value = str(value)
            value = value.replace('\r', '')
            value = value.replace('\x04', '')
            return value

        def ans(self, value):
            if value:
                self._ans += self.fmt(value)

        def err(self, value):
            if value:
                self._err += self.fmt(value)

    for var in args.names:
        out = Output()
        with kernel.device as repl:
            repl.eval(f"import json\nprint(json.dumps(repr({var})))", out)
        if len(out._err.strip()) > 0:
            kernel.error(f"Variable '{var}': {out._err}\n")
            return
        logger.debug(f"{var} = {out._ans}")
        kernel.execute_ipython(f"{var} = eval({out._ans})\n")


@arg('names', nargs='*', help="variable names")
@line_magic
def fromhost_magic(kernel, args):
    """Copy variables from the host to the microcontroller
Only works for variables that can be encoded in json.

Example:
    %%host
    a = 'Hello from host'
    %%connect mcu
    %fromhost a
    print(a)
"""
    for var in args.names:
        code = f"import json\nprint(json.dumps(repr({var})))"
        kernel.execute_ipython(code)