import io
import sys
import pytest
from contextlib import redirect_stdout, redirect_stderr
from lyncs_setuptools import (
    find_version,
    get_kwargs,
    print_keys,
    CMakeExtension,
    CMakeBuild,
    find_package,
)
from lyncs_setuptools.cmake import get_version, get_variables
from lyncs_setuptools.cmake import print_find_package
from distutils.dist import Distribution
from lyncs_setuptools import __version__ as version
from lyncs_setuptools.packages import *


def capture_stdout_and_err(fnc, *args, **kwargs):
    "Captures stdout and stderr returned as two strings"
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out):
        with redirect_stderr(err):
            fnc(*args, **kwargs)
    return out.getvalue(), err.getvalue()


def test_kwargs():
    assert find_version() == version

    out, err = capture_stdout_and_err(print_keys, [])
    assert 'version: "' in out
    assert not err

    out, err = capture_stdout_and_err(print_keys, ["author"])
    assert out == get_kwargs()["author"] + "\n"
    assert not err


def test_cmake():
    dist = Distribution()
    build = CMakeBuild(dist)
    build.extensions = [CMakeExtension("test", "test", ["-DMESSAGE=test1234"])]
    build.build_lib = "test"
    build.build_temp = "test/tmp"

    out, err = capture_stdout_and_err(build.run)
    assert "test1234" in out
    assert not err


def test_cmake_find_package():
    assert "MPI_FOUND" in find_package("MPI", clean=False)
    assert "found" in find_package("MPI")
    sys.argv = ["lyncs_find_package", "foo"]
    out, err = capture_stdout_and_err(print_find_package)
    assert "found: 0" in out.split("\n")
    assert not err


def test_cmake_version():
    assert get_version() == get_variables()["CMAKE_VERSION"]


def test_packages():
    assert "lyncs_setuptools" in lyncs_packages()
    assert f"lyncs-setuptools=={version}" in lyncs_packages_verbose()

    sys.argv = ["lyncs_packages"]
    out, err = capture_stdout_and_err(print_packages)
    assert "lyncs_setuptools" in out
    assert not err

    sys.argv = ["lyncs_packages", "-v"]
    out, err = capture_stdout_and_err(print_packages)
    assert f"lyncs-setuptools=={version}" in out
    assert not err


try:
    from lyncs_setuptools.pylint import print_pylint_badge

    skip_pylint = False
except ModuleNotFoundError:
    skip_pylint = True


@pytest.mark.skipif(skip_pylint, reason="lyncs_setuptools[pylint] not installed")
def test_pylint():
    sys.argv = ["lyncs_pylint_badge", "."]
    out, err = capture_stdout_and_err(print_pylint_badge, do_exit=False)
    assert "[![pylint](https://img.shields.io/badge" in out
    assert "Your code has been rated" in err
