#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pathlib import Path

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    version = Path(package, "__version__.py").read_text()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", version).group(1)


def get_long_description():
    """
    Return the README.
    """
    long_description = ""
    with open("README.md", encoding="utf8") as f:
        long_description += f.read()
    long_description += "\n\n"
    with open("CHANGELOG.md", encoding="utf8") as f:
        long_description += f.read()
    return long_description


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [str(path.parent) for path in Path(package).glob("**/__init__.py")]


setup(
    name="zodb-cm",
    python_requires=">=3.6",
    version=get_version("zcm"),
    url="https://github.com/baloan/zodb-cm",
    project_urls={
        "Changelog": "https://github.com/baloan/zodb-cm/CHANGELOG.md",
        "Documentation": "https://...",
        "Source": "https://github.com/baloan/zodb-cm",
    },
    license="MIT",
    description="ZODB context manager",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Andreas Balogh",
    author_email="baloand@gmail.com",
    zip_safe=False,
    install_requires=[
        "ZODB",
        "ZEO",
    ],
    extras_require={
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: ZODB",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
    ],
)
