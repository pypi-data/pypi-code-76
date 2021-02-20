"""Support Function."""
import cpuinfo as _cpuinfo
import numpy as _numpy

import numpy_ipps._detail.libipp as _libipp
import numpy_ipps.utils


class CacheParams:
    """Cache parameters Function."""

    _ipp_types = ("Data", "Instruction", "Unified")

    def __init__(self):
        if not hasattr(_libipp.ipp_core, "ippGetCacheParams"):
            _libipp.ffi.cdef(
                """
                typedef struct {
                    int type, level, size;
                } IppCache;
            """
            )
            _libipp.ffi.cdef("int ippGetCacheParams(IppCache**);")

    def __call__(self):
        ipp_caches = numpy_ipps.utils.new("IppCache**")
        numpy_ipps.status = _libipp.ipp_core.ippGetCacheParams(ipp_caches)

        index = 0

        if ipp_caches[0][index].type == 0:
            info = _cpuinfo.get_cpu_info()
            if "l1_data_cache_size" in info:
                yield "Data", 1, info["l1_data_cache_size"]
            else:
                yield "Data", 1, info["l2_cache_size"] // info[
                    "l2_cache_associativity"
                ]
            yield "Unified", 2, info["l2_cache_size"]
            yield "Unified", 3, info["l3_cache_size"]
            return

        while ipp_caches[0][index].type != 0:
            yield CacheParams._ipp_types[
                ipp_caches[0][index].type - 1
            ], ipp_caches[0][index].level, ipp_caches[0][index].size
            index += 1


cache_params = CacheParams()
L1 = _numpy.min([cache_size for _u0, _u1, cache_size in cache_params()])


class CpuFeatures:
    """CPU features Function."""

    _ipp_features = (
        "MMX",
        "SSE",
        "SSE 2",
        "SSE 3",
        "SSSE 3",
        "MOVBE",
        "SSE 4.1",
        "SSE 4.2",
        "AVX (CPU)",
        "AVX (OS)",
        "AES",
        "CLMUL",
        "UNDEF",
        "RDRAND",
        "FP16",
        "AVX 2",
        "ADX",
        "RDSEED",
        "PREFETCHW",
        "SHA",
        "AVX 512",
        "AVX 512 (CD)",
        "AVX 512 (ER)",
        "Xeon Phi",
    )

    def __init__(self):
        if not hasattr(_libipp.ipp_core, "ippGetEnabledCpuFeatures"):
            _libipp.ffi.cdef("uint64_t ippGetEnabledCpuFeatures();")

    def __call__(self):
        enabled_features = _libipp.ipp_core.ippGetEnabledCpuFeatures()

        for bit, feature in enumerate(CpuFeatures._ipp_features):
            if enabled_features & (1 << bit):
                yield feature


cpu_features = CpuFeatures()


class CpuFreq:
    """CPU frequency Function."""

    def __init__(self):
        if not hasattr(_libipp.ipp_core, "ippGetCpuFreqMhz"):
            _libipp.ffi.cdef("int ippGetCpuFreqMhz(int*);")

    def __call__(self):
        ipp_freq = numpy_ipps.utils.new("int*")
        numpy_ipps.status = _libipp.ipp_core.ippGetCpuFreqMhz(ipp_freq)

        return ipp_freq[0] * 1e6


cpu_frequency = CpuFreq()


class LibVersion:
    """Library version Function."""

    def __init__(self):
        if not hasattr(_libipp.ipp_core, "ippGetLibVersion"):
            _libipp.ffi.cdef(
                """
                typedef struct {
                    int major, minor, majorBuild, build;
                    char targetCpu[4];
                    char *Name, *Version, *BuildDate;
                } IppLibraryVersion;
            """
            )
            _libipp.ffi.cdef("IppLibraryVersion* ippGetLibVersion();")

    def __call__(self):
        ipp_lib_version = _libipp.ipp_core.ippGetLibVersion()

        return (
            ipp_lib_version[0].major,
            ipp_lib_version[0].minor,
            ipp_lib_version[0].majorBuild,
            _libipp.ffi.string(ipp_lib_version[0].targetCpu).decode("UTF-8"),
            _libipp.ffi.string(ipp_lib_version[0].Name).decode("UTF-8"),
            _libipp.ffi.string(ipp_lib_version[0].Version).decode("UTF-8"),
            _libipp.ffi.string(ipp_lib_version[0].BuildDate).decode("UTF-8"),
        )


library_version = LibVersion()
