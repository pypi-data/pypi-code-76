import os
import sys

import setuptools
from setuptools import find_packages, setup

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MSEplots_pkg",
    version="2.5.1",
    author="Wei-Ming Tsai",
    author_email="wxt108@rsmas.miami.edu",
    description="A package for static energy plots based on MetPy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weiming9115/MSEplots",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['metpy']
)
