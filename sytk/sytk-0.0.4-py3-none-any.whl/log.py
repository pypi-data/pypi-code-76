import functools
from contextlib import redirect_stdout
import inspect
import datetime
import traceback
import sys


class _StdoutHandler:
    def __init__(self, stdout):
        self.stdout = stdout

    def write(self, text):
        if text != '\n':
            self.stdout.write(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")}]\n{text}')
        self.stdout.write('\n')

    def close(self):
        self.stdout.close()


class _Log:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        with open(f'{inspect.stack()[2].filename.replace(".", "_")}_{self.func.__name__}.log', 'a') as f:
            with redirect_stdout(f):
                sys.stdout = _StdoutHandler(sys.stdout)
                try:
                    result = self.func(*args, **kwargs)
                    return result
                except Exception:
                    print(traceback.format_exc())


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _Log(func)(*args, **kwargs)

    return wrapper

