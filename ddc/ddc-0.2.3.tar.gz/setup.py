#!/usr/bin/env python
import io
import os
import sys

import setuptools
from setuptools import setup
from ddc import info

if sys.version_info < (3, 6, 0):
    print("Python 3.6+ is required")  # noqa
    exit(1)

here = os.path.abspath(os.path.dirname(__file__))
cur_dir = os.path.realpath(os.path.dirname(__file__))

with io.open(os.path.join(cur_dir, "requirements.txt")) as requirements_file:
    requirements = requirements_file.read().strip().split("\n")

setup(
    name=info.__package_name__,
    version=info.__version__,
    entry_points={"console_scripts": ["ddc=ddc.cli:main"]},
    description="Devision Developers Cli",
    long_description="",
    url="https://github.com/devision-io/ddc",
    author="Devision",
    author_email="info@devision.io",
    license="Apache 2.0",
    zip_safe=False,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=requirements,
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    package_data={"": ["LICENSE"]},
    platforms="Posix; MacOS X; Windows",
    include_package_data=True,
)
