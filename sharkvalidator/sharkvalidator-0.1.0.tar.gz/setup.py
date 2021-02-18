# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-02-18 13:52

@author: johannes

"""
import os
import setuptools


def long_description():
    if os.path.exists('README.rst'):
        return open('README.rst').read()
    else:
        return 'No readme file'


setuptools.setup(
    name="sharkvalidator",
    version="0.1.0",
    author="Johannes Johansson",
    author_email="johannes.johansson@smhi.se",
    description="Validate data delivery at the Swedish NODC",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
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
)
