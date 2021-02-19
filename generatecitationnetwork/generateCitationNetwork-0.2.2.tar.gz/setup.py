#!/usr/bin/env python

import os
import sys

from setuptools import find_packages, setup

# ADD needed libraries needed for the end user of the package:
# example:
#      requirements = ["numpy", "scipy>=1.0.0", "requests==2.0.1"

requirements = [
    'pandas',
    'numpy',
    'pysolr',
    'nbsphinx',
    'textacy',
    'nltk',
    'srsly'
]


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog", "")


doclink = """
Documentation
-------------

The full documentation can be generated with Sphinx"""


PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name="generateCitationNetwork",
    version="0.2.2",
    description="""
        A tool to generate a network of cited and
        referenced papers for a given DOI.
    """,
    long_description=readme + "\n\n" + doclink + "\n\n" + history,
    author="Malte Vogl",
    author_email="mvogl@mpiwg-berlin.mpg.de",
    url="https://gitlab.gwdg.de/GMPG/generatecitationnet",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    keywords="generateCitationNetwork",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
)
