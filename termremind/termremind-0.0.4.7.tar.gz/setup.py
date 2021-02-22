#!/usr/bin/env python3

"""
Setup file
"""

import os

from setuptools import find_packages, setup

from termremind.main import getver

with open("README.md") as f:
    ld = f.read()

setup(
    name="termremind",
    version=getver(),
    description="Reminders in terminal",
    long_description=ld,
    long_description_content_type="text/markdown",
    keywords="python3 linux system-information",
    url="https://github.com/SomethingGeneric/Remind",
    author="Matt C",
    author_email="matt@mattcompton.me",
    license="GPLv3",
    packages=find_packages(),
    python_requires=">=3",
    install_requires=["colorama"],
    entry_points={"console_scripts": ["remind = termremind.main:main"]},
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System",
        "Topic :: Terminals",
    ],
)
