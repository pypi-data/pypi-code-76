#!/usr/bin/env python3
import pathlib
from setuptools import setup

# Package meta-data
NAME = 'jtlib'
DESCRIPTION = 'Utility library'
URL = 'https://github.com/joeyturczak/jtlib'
EMAIL = 'joeyturczak@gmail.com'
AUTHOR = 'Joey Turczak'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'
LICENSE = 'MIT'

# Required packages
REQUIRED = [
    'pandas'
]

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    packages=['jtlib'],
    install_requires=REQUIRED,
    include_package_data=True,
    license=LICENSE
)