import os
import sys

import cffi


ffi = cffi.FFI()

if sys.platform.startswith("win32"):
    try:
        ipp_core = ffi.dlopen("ippcore.dll")
        ipp_libraries = (ffi.dlopen("ipps.dll"), ffi.dlopen("ippvm.dll"))
    except OSError:
        _base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "lib",
            "win32",
        )
        ipp_core = ffi.dlopen(os.path.join(_base_path, "ippcore.dll"))
        for lib in os.listdir(_base_path):
            ffi.dlopen(os.path.join(_base_path, lib))
        ipp_libraries = (
            ffi.dlopen(os.path.join(_base_path, "ipps.dll")),
            ffi.dlopen(os.path.join(_base_path, "ippvm.dll")),
        )
elif sys.platform.startswith("darwin"):
    ipp_core = ffi.dlopen("libippcore.dylib")
    ipp_libraries = (ffi.dlopen("libipps.dylib"), ffi.dlopen("libippvm.dylib"))
else:
    try:
        ipp_core = ffi.dlopen("libippcore.so")
        ipp_libraries = (ffi.dlopen("libipps.so"), ffi.dlopen("libippvm.so"))
    except OSError:
        _base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "lib",
            "linux",
        )
        ipp_core = ffi.dlopen(os.path.join(_base_path, "libippcore.so"))
        for lib in os.listdir(_base_path):
            ffi.dlopen(os.path.join(_base_path, lib))
        ipp_libraries = (
            ffi.dlopen(os.path.join(_base_path, "libipps.so")),
            ffi.dlopen(os.path.join(_base_path, "libippvm.so")),
        )

if not hasattr(ipp_core, "ippInit"):
    ffi.cdef("int ippInit();")
    ffi.cdef(
        """
    typedef enum {
        ippAlgHintNone,
        ippAlgHintFast,
        ippAlgHintAccurate
    } IppHintAlgorithm;
    """
    )
