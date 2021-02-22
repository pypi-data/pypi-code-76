#!/usr/bin/env python
"""setup.py for cmemc."""

from setuptools import setup, find_packages

setup(
    name="cmem_cmemc",
    version="21.02",
    author="eccenca",
    author_email="cmempy-developer@eccenca.com",
    maintainer="Sebastian Tramp",
    maintainer_email="sebastian.tramp@eccenca.com",
    url="https://eccenca.com/go/cmemc",
    description="Command line client for eccenca Corporate Memory",
    long_description=open("README-public.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="Apache 2.0",
    entry_points={
        "console_scripts": [
            "cmemc = cmem.cmemc.cli:main",
        ],
    },
    install_requires=[
        "certifi",
        "click",
        "click_help_colors",
        "click-didyoumean",
        "configparser",
        "Jinja2",
        "natsort",
        "Pygments",
        "requests",
        "tabulate",
        "timeago",
        "treelib",
        "urllib3",
        "six",
        "cmem-cmempy"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Testing",
        "Topic :: Database",
        "Topic :: Utilities",
    ],
)
