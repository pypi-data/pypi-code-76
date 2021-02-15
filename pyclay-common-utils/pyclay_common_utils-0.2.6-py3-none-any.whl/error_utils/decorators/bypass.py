from functools import wraps
import sys
import traceback

def bypass_error_in_classmethod(print_func=print):
    def inner(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                method(self, *args, **kwargs)
            except:
                etype, evalue, tb = sys.exc_info()
                e = traceback.format_tb(tb=tb)
                print_func(''.join(e[1:]))
        return wrapper
    return inner

def bypass_error_in_func(print_func=print):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                etype, evalue, tb = sys.exc_info()
                e = traceback.format_tb(tb=tb)
                print_func(''.join(e[1:]))
        return wrapper
    return inner