# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-02-18 13:52

@author: johannes

[![PyPi version](https://pypip.in/v/sharkvalidator/badge.png)](https://crate.io/packages/sharkvalidator/)
[![PyPi wheel](https://pypip.in/wheel/sharkvalidator/badge.png)](https://crate.io/packages/sharkvalidator/)
[![PyPi license](https://pypip.in/license/sharkvalidator/badge.png)](https://crate.io/packages/sharkvalidator/)


SHARKvalidator
=====
.. image:: https://pypip.in/v/sharkvalidator/badge.png
    :target: https://pypi.python.org/pypi/sharkvalidator/
    :alt: Latest PyPI version

.. image:: https://pypip.in/wheel/sharkvalidator/badge.svg
    :target: https://pypi.python.org/pypi/sharkvalidator/

.. image:: https://pypip.in/license/sharkvalidator/badge.svg
    :target: https://pypi.python.org/pypi/sharkvalidator/

"""
import os
import setuptools


NAME = 'sharkvalidator'
README = open('README.rst', 'r').read()

setuptools.setup(
    name=NAME,
    version="0.1.6",
    author="SMHI - NODC",
    author_email="shark@smhi.se",
    description="Validate data delivery at the Swedish NODC",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sharksmhi/sharkvalidator",
    packages=setuptools.find_packages(),
    package_data={'sharkvalidator': [
        os.path.join('etc', '*.xlsx'),
        os.path.join('etc', 'readers', '*.yaml'),
        os.path.join('etc', 'validators', '*.yaml'),
        os.path.join('etc', 'writers', '*.yaml'),
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
