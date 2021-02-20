#!/usr/bin/env python

import os
import setuptools
import ghm.meta as meta

setuptools.setup(
    name=meta.NAME,
    version=meta.VERSION,
    author=meta.AUTHOR,
    author_email=meta.EMAIL,
    description=meta.DESCRIPTION,
    long_description=open(os.path.join(
        os.path.dirname(__file__),
        "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mconigliaro/ghm",
    packages=setuptools.find_packages(),
    scripts=["bin/ghm"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: System :: Systems Administration"
    ],
    python_requires=">=3.6",
    install_requires=[
        "pygit2 >=1.4, <2.0",
        "PyGithub >=1.5.3, <2.0"
    ],
)
