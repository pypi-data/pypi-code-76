"""
Simple hello example using an external C library.
"""
import ctypes as ct
import platform
import glob
import os

_lib = ct.cdll.LoadLibrary(glob.glob(os.path.join(__path__[0],'ext.*'))[0])
_lib.hello.argtypes = [ct.c_char_p]
_lib.hello.restype = ct.c_void_p
_lib.release.argtypes = [ct.c_void_p]

def hello(name: str) -> str:
    """
    hello(name) returns "hello "+name+"!".

    An exception is thrown when the argument is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("hello() argument must be of type string")
    res_allocated = _lib.hello(name.encode('utf8'))
    # from https://marc.info/?l=python-list&m=159159464309156&w=2
    res = ct.string_at(res_allocated).decode('utf-8')
    _lib.release(res_allocated)
    return res
