import functools
import datetime
import inspect


class _Debug:
    register = dict()

    def __init__(self, func):
        self.func = func
        self.register[func.__name__] = self

    def __call__(self, *args, **kwargs):
        print(f'\x1b[38;5;117m'
              f'[{datetime.datetime.now().strftime("%H:%M:%S")}]'
              f'\x1b[0;m', end=' ')
        print(f'\x1b[38;5;117m'
              f'"{self.func.__name__}" was called:\n'
              f'Caller: {inspect.stack()[2].function}\n'
              f'Params: {args, kwargs}'
              f'\x1b[0;m')

        print(f'\x1b[38;5;117m'
              f'Loc: line {inspect.stack()[2].lineno} in "{inspect.stack()[2].filename}"'
              f'\x1b[0;m')

        result = self.func(*args, **kwargs)

        print(f'\x1b[38;5;117m'
              f'[{datetime.datetime.now().strftime("%H:%M:%S")}]'
              f'\x1b[0;m', end=' ')
        print(f'\x1b[38;5;117m'
              f'"{self.func.__name__}" returned with: {result}'
              f'\n'
              f'\x1b[0;m')

        return result


def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _Debug(func)(*args, **kwargs)
    return wrapper


def d_print(*args, **kwargs):
    caller = inspect.stack()[1].function
    if caller in _Debug.register.keys():
        print(f'\x1b[38;5;117m'
              f'[{datetime.datetime.now().strftime("%H:%M:%S")}]'
              f'\x1b[0;m', end=' ')
        print(f'\x1b[38;5;117m', end='')
        print(*args, **kwargs, end='')
        print(f'\x1b[0;m')
