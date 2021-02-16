#!/usr/bin/env python

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='strtest',
    version='0.1.0',
    description='Runs test code contained in strings',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Andrew Kurauchi',
    author_email='andrewtnk@insper.edu.br',
    url='https://github.com/Insper/python-string-test-runner',
    packages=['strtest'],
    scripts=['run_str_test.py'],
    license="MIT",
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
