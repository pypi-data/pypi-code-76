
from types import FunctionType


def test_load_function():
    foo_code = compile('def foo(): return {result:"bar"}', "dic", "exec")
    foo_func = FunctionType(foo_code.co_consts[0], globals(), "foo")
    # test = exec(foo_code)
    var = foo_func()
    print(var)
