# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-02-18 13:52

@author: johannes

"""
import os
import setuptools


NAME = 'sharkvalidator'
README = open('README.rst', 'r').read()

setuptools.setup(
    name=NAME,
    version="0.1.2",
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
