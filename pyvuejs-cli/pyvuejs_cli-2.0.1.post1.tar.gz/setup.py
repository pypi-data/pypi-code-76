#!/usr/bin/env python

from setuptools import setup, find_packages  # type: ignore
from pyvuejs_cli import __version__

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as require_file:
    requires = require_file.readlines()

setup(
    author="eseunghwan",
    author_email="shlee0920@naver.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    description="pyvuejs cli",
    entry_points={"console_scripts": ["pyvuejs_cli=pyvuejs_cli.cli:main",],},
    install_requires=requires,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_data={
        "": [
            "*.zip"
        ]
    },
    include_package_data=True,
    keywords="pyvuejs_cli",
    name="pyvuejs_cli",
    packages=["pyvuejs_cli"],
    setup_requires=requires,
    url="https://github.com/eseunghwan/pyvuejs_cli",
    version=__version__,
    zip_safe=False,
)
