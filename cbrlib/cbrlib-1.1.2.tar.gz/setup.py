import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cbrlib",
    version="1.1.2",
    description="Library for the implementation of projects with the help of Case Based Reasoning",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hilfestellung/PyCBR",
    author="Christian Dein",
    author_email="christian.dein@dein-hosting.de",
    license="LGPL-2.1-or-later",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["cbrlib.evaluation", "cbrlib.model", "cbrlib.reasoning", "cbrlib.utils"],
    include_package_data=True,
    install_requires=["PyYAML"],
)
