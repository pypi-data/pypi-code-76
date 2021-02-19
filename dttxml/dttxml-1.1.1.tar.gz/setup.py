#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import os
import sys
import setup_helper

from setuptools import find_packages, setup

version = '1.1.1'
cmdclass = setup_helper.version_checker(version, 'dttxml')


setup(
    name='dttxml',
    license = 'Apache v2',
    version=version,
    url='https://git.ligo.org/cds/dttxml',
    author='Lee McCuller',
    author_email='Lee.McCuller@ligo.org',
    description=(
        'Extract data from LIGO Diagnostics test tools XML format. Formerly dtt2hdf.'
    ),
    packages=find_packages(exclude=['doc']),
    install_requires = [
        'numpy', 'h5py',
        'declarative>=1.2.0',
    ],
    extras_require   ={
        "hdf" : ["h5py"],
    },
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dtt2hdf=dttxml.dtt2hdf:main',
        ]},
    cmdclass       = cmdclass,
    zip_safe       = True,
    keywords = 'LIGO dtt diagnostics file-reader',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
