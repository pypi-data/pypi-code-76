#!/usr/bin/env python3

import distutils.text_file
import logging
import os
from pathlib import Path
from typing import List

import setuptools

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

# Package meta-data.
NAME = "hash-artifacts"
DESCRIPTION = "Compute a combined hash for the given artifact paths (that can include glob patterns)"
URL = "https://gitlab.com/gherasmann/maak-menu/scripts/hash-artifacts"
EMAIL = "developer@gherasmann.com"
AUTHOR = "Gherasmann"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.1"


REQUIRED = ["pyfunctional"]

here = os.path.abspath(os.path.dirname(__file__))

env_suffix = os.environ.get("ENVIRONMENT_SUFFIX", "")
logger.info(f"Environment suffix: {env_suffix}")

if env_suffix is not None and len(env_suffix) > 0:
    NAME += f"-{env_suffix}"

logger.info(f"Package name: {NAME}")

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    description=DESCRIPTION,
    packages=setuptools.find_packages(
        exclude=["tests", "*.tests", "*.tests", "tests.*"]
    ),
    include_package_data=True,
    license="MIT",
    install_requires=REQUIRED,
    entry_points={
        "console_scripts": ["hash-artifacts = hash_artifacts.hash_artifacts:main"]
    },
    python_requires=">=3.6",
)
