"""
This script is the minimal script to build distribution files.

setuptools.setup() looks for configuration information in setup.cfg.
"""
import setuptools
from codecs import open
import os

setuptools.setup()

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    ld = f.read()

long_description = ld
description = "action scheduling api, sdk"