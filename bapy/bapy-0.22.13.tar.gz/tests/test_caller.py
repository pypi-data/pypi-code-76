# coding=utf-8
import asyncio
import inspect
from icecream import ic
from icecream import IceCreamDebugger

from bapy import aioloop
from bapy import AsDict
from bapy import caller
from bapy import ipaddr

ic.enable()


def exclude(d, data_attrs: tuple[str, tuple] = None):
    if isinstance(d, str):
        if d.startswith('__'):
            return True

    if data_attrs:
        if data_attrs[0] not in data_attrs[1]:
            return True

    if any([inspect.ismodule(d), inspect.isroutine(d), isinstance(d, property)]):
        return True

# v = {
#     'open': {
#         'ip': {},
#         'sctp': {},
#         'tcp': {
#             80: {'open': True, 'script': {}, 'service': 'http'},
#             443: {'open': True, 'script': {}, 'service': 'https'}
#         },
#         'udp': {}
#     },
#     'filtered': {
#         'ip': {},
#         'sctp': {1: 'http'},
#         'tcp': {
#             80: {'open': True, 'script': {}, 'service': 'http'},
#             443: {'open': True, 'script': {}, 'service': 'https'}
#         },
#         'udp': {
#             80: {'open': True, 'script': {}, 'service': 'https'},
#             72: {'open': True, 'script': {'a': 4}, 'service': 'https'}
#         }
#     }
# }
# ic(Nested(v, 0, 'service'))
# assert not Nested(v, 0, 'service').values('x')
# assert Nested(v, 0, 'service').exclude('service')
# assert not dpath.util.search(Nested(v, 0, 'service').run(), '**/service')
# assert not dpath.util.search(Nested(v, 0, values='http').run(), '**', afilter=lambda x: 'http' == x)
# assert not dpath.util.search(Nested(v, 0, 'service', values='http').run(), '**', afilter=lambda x: 'http' == x)


# noinspection PyUnusedLocal
def arg(b, x=1, *args, **kwargs):
    return caller(1, depth=1)


def test_caller():
    class A(AsDict):
        g = 1

        def __init__(self):
            self.a_1 = 1

        def a(self):
            self.a_1 = 2
            index = 3
            c = caller(index, depth=2)
            ic('a', c.funcname, index, c.coro, c.qual, c.vars)
            c = caller(3, depth=2)
            assert not c.coro
            assert c.funcname == '<module>'
            assert not c.qual
            assert c.vars.glob['ic']['lineWrapWidth'] == 70
            assert c.vars.loc['ic']['lineWrapWidth'] == 70
            c = caller(3, depth=1)
            assert isinstance(c.vars.glob['ic'], IceCreamDebugger)
            assert isinstance(c.vars.loc['ic'], IceCreamDebugger)

        # @property
        # def b(self):
        #     print()
        #     index = 2
        #     c = caller(index, depth=1)
        #     ic('c', index, c.coro, c.qual, c.vars)
        #     if c.funcname == 'd':
        #         assert not c.coro
        #     if c.funcname == 'locs_':
        #         assert not c.coro
        #     if c.funcname == 'f':
        #         assert c.coro
        #     return c
        #
        # async def c(self):
        #     self.d()
        #     print()
        #     index = 1
        #     c = caller(index, depth=3)
        #     ic('c', index, c.coro, c.qual, c.vars)
        #     print()
        #     index = 2
        #     c = caller(index)
        #     ic('c', index, c.coro, c.funcname, c.coro, c.qual, c.vars)
        #     if c.funcname == 'locs_':
        #         assert not c.coro
        #     if c.funcname == 'f':
        #         assert c.coro
        #     return c
        #
        # @classmethod
        # def d(cls):
        #     func = caller(1).funcname
        #     print()
        #     index = 1
        #     c = caller(index, depth=2)
        #     ic(func, index, c.coro, c.qual, c.vars)
        #     print()
        #     ic(cls().b)
        #     return c
        #
        # @staticmethod
        # def e():
        #     if aioloop():
        #         ic(asyncio.current_task().get_name())
        #     index = 2
        #     c = caller(index, depth=2)
        #     ic('e', index, c.coro, c.qual, c.vars)
        #     if c.funcname == 'f':
        #         assert c.coro
        #     if c.funcname == 'locs_':
        #         assert not c.coro
        #     return c
        #
        # @property
        # async def f(self):
        #     print()
        #     index = 1
        #     c = caller(index, depth=2)
        #     ic('ff', index, c.coro, c.qual, c.vars)
        #     index = 2
        #     c = caller(index)
        #     ic('f', index, c.funcname, c.coro, c.qual, c.vars)
        #     self.e()
        #     _ = self.b
        #
        #     return c

    obj = A()
    obj.a()
    # _ = obj.b
    # asyncio.run(obj.c(), debug=False)
    # A.d()
    # obj.e()
    # asyncio.run(obj.f, debug=False)


def test_arg():
    arg_caller_local = arg(2)
    assert arg_caller_local.funcname == arg.__name__
    assert arg_caller_local.coro is None
    assert arg_caller_local.args == {'b': 2, 'x': 1}
    assert arg(3, 7, 9).args == {'args': (9,), 'b': 3, 'x': 7}
    assert arg(3, 7, 9, first=2, second=3).args == {'args': (9,), 'b': 3, 'first': 2, 'second': 3, 'x': 7}
    assert arg(3, 8, 7, first=2, second=3).args == {'args': (7,), 'b': 3, 'first': 2, 'second': 3, 'x': 8}
    assert arg(3, 8, first=2, second=3).args == {'b': 3, 'first': 2, 'second': 3, 'x': 8}


