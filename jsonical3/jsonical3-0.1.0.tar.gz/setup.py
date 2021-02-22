#
# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the nebgb package released under the MIT license.
#

from setuptools import setup

long_desc = """
Canonical serializations for JSON.

Similar to the basic API for the `json`/`simplejson` modules with
a few restrictions on modifiying serialization.
"""

setup(
    name="jsonical3",
    description="Canonical JSON for Python 3",
    long_description=long_desc,
    author="Paul Joseph Davis",
    author_email="paul.joseph.davis@gmail.com",
    maintainer="Lane Shaw",
    maintainer_email="lshaw.tech@gmail.com",
    url="https://github.com/LanetheGreat/jsonical3",
    version="0.1.0",
    license="MIT",
    keywords="JSON canonical serialization",
    platforms=["any"],
    zip_safe=True,
    py_modules=["jsonical3"],
)
