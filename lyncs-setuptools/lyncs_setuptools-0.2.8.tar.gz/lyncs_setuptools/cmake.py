"""
Tools for running CMake in setup phase
"""

__all__ = [
    "CMakeExtension",
    "CMakeBuild",
    "find_package",
]

import argparse
import os
import subprocess
from tempfile import TemporaryDirectory
from setuptools import Extension
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    "Setup extension for CMake"

    def __init__(self, name, source_dir=".", cmake_args=None, post_build=None):
        source_dir = source_dir or "."

        sources = [source_dir + "/CMakeLists.txt"]
        if os.path.exists(source_dir + "/patches"):
            for filename in os.listdir(source_dir + "/patches"):
                sources += [source_dir + "/patches/" + filename]

        Extension.__init__(self, name, sources=sources)
        self.source_dir = os.path.abspath(source_dir)
        self.cmake_args = (
            [cmake_args] if isinstance(cmake_args, str) else (cmake_args or [])
        )
        self.post_build = post_build


class CMakeBuild(build_ext):
    "Build phase of the CMakeExtension"

    def run(self):
        "build_ext function that manages the installation"
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_extension(ext)
                self.extensions.remove(ext)
        if self.extensions:
            build_ext.run(self)

    def get_install_dir(self, ext):
        "Returns the installation directory (the module base directory)"
        return os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

    def build_extension(self, ext):
        "Runs the CMake scripts in the build phase"

        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError as err:
            raise OSError(
                "CMake must be installed to build the following extensions: " + ext.name
            ) from err

        cmake_args = ["-DEXTERNAL_INSTALL_LOCATION=" + self.get_install_dir(ext)]
        cmake_args += ext.cmake_args

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
        build_args += ["--", "-j", str(abs(os.cpu_count() - 1) or 1)]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        out = subprocess.check_output(
            ["cmake", ext.source_dir] + cmake_args, cwd=self.build_temp, env=env
        )
        out += subprocess.check_output(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )
        print(out.decode())

        if ext.post_build:
            ext.post_build(self, ext)


def get_version():
    """Returns CMake version"""
    out = subprocess.check_output(
        ["cmake", "--version"], stderr=subprocess.DEVNULL
    ).decode()
    for part in out.split():
        if part[0].isdigit():
            return part
    raise RuntimeError("Could not deduce version")


CMAKE_FIND = """
cmake_minimum_required(VERSION ${CMAKE_VERSION})

project(LYNCS)

get_cmake_property(_before VARIABLES)

find_package(%s)

get_cmake_property(_after VARIABLES)
foreach (_name ${_after})
    if((NOT _name IN_LIST _before) AND (NOT _name STREQUAL "_before"))
      message(STATUS "VAR ${_name} = ${${_name}}")
    endif()
endforeach()
"""


def parse_value(val):
    "Parse a CMake value"
    if not isinstance(val, str):
        return val
    try:
        return int(val)
    except ValueError:
        pass
    if ";" in val:
        return val.split(";")
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    return val


def find_package(name, clean=True):
    """
    Returns the output of find_package by CMake.
    If clean, returns post-processed values.
    Otherwise all the variables and value from CMake.
    """

    with TemporaryDirectory() as temp_dir:
        with open(temp_dir + "/CMakeLists.txt", "w") as cmake_file:
            cmake_file.write(CMAKE_FIND % name)

        out = subprocess.check_output(
            ["cmake", "."], cwd=temp_dir, stderr=subprocess.DEVNULL
        )

    lines = tuple(
        line.split()[2:]
        for line in out.decode().split("\n")
        if line.startswith("-- VAR")
    )
    assert all((len(line) >= 2 and "=" in line for line in lines))

    values = {line[0]: " ".join(line[2:]) if len(line) >= 3 else None for line in lines}

    if not clean:
        return values

    return {
        key[len(name) + 1 :].lower(): parse_value(val)
        for key, val in values.items()
        if key.startswith(name + "_")
    }


def print_find_package():
    "Returns the values of find_package"
    parser = argparse.ArgumentParser(
        "Returns the variables defined by CMake find_package"
    )
    parser.add_argument("package", nargs=1, help="The package to find, e.g. MPI")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="prints all the values without cleaning them",
    )
    args = parser.parse_args()
    out = find_package(args.package[0], clean=args.verbose == 0)

    for key, val in out.items():
        print(key + ":", val)


CMAKE_VARS = """
cmake_minimum_required(VERSION ${CMAKE_VERSION})

project(LYNCS)

get_cmake_property(_vars VARIABLES)

foreach (_name ${_vars})
    if(NOT _name STREQUAL "_vars")
      message(STATUS "VAR ${_name} = ${${_name}}")
    endif()
endforeach()
"""


def get_variables():
    """
    Returns the output of find_package by CMake.
    If clean, returns post-processed values.
    Otherwise all the variables and values from CMake.
    """

    with TemporaryDirectory() as temp_dir:
        with open(temp_dir + "/CMakeLists.txt", "w") as cmake_file:
            cmake_file.write(CMAKE_VARS)

        out = subprocess.check_output(
            ["cmake", "."], cwd=temp_dir, stderr=subprocess.DEVNULL
        )

    lines = tuple(
        line.split()[2:]
        for line in out.decode().split("\n")
        if line.startswith("-- VAR")
    )
    assert all((len(line) >= 2 and "=" in line for line in lines))

    values = {line[0]: " ".join(line[2:]) if len(line) >= 3 else None for line in lines}

    return {key: parse_value(val) for key, val in values.items()}
