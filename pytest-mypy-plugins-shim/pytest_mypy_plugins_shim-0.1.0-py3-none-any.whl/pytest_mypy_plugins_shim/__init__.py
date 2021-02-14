#!/usr/bin/env python3
#
#  __init__.py
"""
Substitute for "pytest-mypy-plugins" for Python implementations which aren't supported by mypy.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
# Based on https://github.com/TypedDjango/pytest-mypy-plugins
# Copyright 2018 Maksim Kurnikov
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import tempfile

# 3rd party
from _pytest.config.argparsing import Parser  # nodep

__all__ = ["pytest_addoption"]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.0"
__email__: str = "dominic@davis-foster.co.uk"


def pytest_addoption(parser: Parser) -> None:  # noqa: D103
	group = parser.getgroup("mypy-tests")
	group.addoption(
			"--mypy-testing-base",
			type=str,
			default=tempfile.gettempdir(),
			help="Base directory for tests to use",
			)

	group.addoption(
			"--mypy-ini-file",
			type=str,
			help="Which .ini file to use as a default config for tests",
			)

	group.addoption(
			"--mypy-same-process",
			action="store_true",
			help="Run in the same process. Useful for debugging, will create problems with import cache",
			)

	group.addoption(
			"--mypy-extension-hook",
			type=str,
			help="Fully qualifield path to the extension hook function, in case you need custom yaml keys. "
			"Has to be top-level.",
			)
