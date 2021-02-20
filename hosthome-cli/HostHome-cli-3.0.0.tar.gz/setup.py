#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = [
    "requests",
    "warn",
    "termcolor",
    "docopt",
    "inquirer"
]


setup(
    name="HostHome-cli",
    version="3.0.0",
    description="HostHome-cli para empezar con el host",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Maubg",
    url="https://github.com/HostHome-oficial/python-CLI",
    include_package_data=True,
    install_requires=requirements,
    packages=[
        "hosthome",
    ],
    license="GNU",
    zip_safe=False,
    keywords="host, hosthome, maubg, python, py, hosty, hoster, home",
    entry_points={
        "console_scripts": ["hosthome=hosthome.comandos:main"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha", "Environment :: Console",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ]
)
