from setuptools import setup, find_packages

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir

import sys

__version__ = "1.1"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension("PyLFMF._cppkernel._cppkernel",
        [ 
          "./PyLFMF/_cppkernel/src/Airy.cpp",
          "./PyLFMF/_cppkernel/src/FlatEarthCurveCorrection.cpp",
          "./PyLFMF/_cppkernel/src/LFMF.cpp",
          "./PyLFMF/_cppkernel/src/ResidueSeries.cpp",
          "./PyLFMF/_cppkernel/src/WiRoot.cpp",
          "./PyLFMF/_cppkernel/src/werf.cpp",
          "./PyLFMF/_cppkernel/src/main.cpp",
          "./PyLFMF/_cppkernel/src/ValidateInputs.cpp"],
        define_macros = [('VERSION_INFO', __version__)],
        ),
]

setup(
    name="PyLFMF",
    version=__version__,
    author="Kirill Savina & Daniel Sherstnev",
    author_email="ksavina@nes.ru",
    url="https://github.com/ksavina/PyLFMF/",
    description="A wrapper for NTIA/LFMF's groundwave propagarion tool",
    long_description="",
    ext_modules=ext_modules,
    packages=['PyLFMF', 'PyLFMF._cppkernel'],
    cmdclass={"build_ext": build_ext},
    zip_safe=False
)
