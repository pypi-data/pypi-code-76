#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists, dirname, realpath
from setuptools import setup, find_packages
import sys


author = u"Paul Müller"
authors = [author]
description = 'Fit and superimpose structures from different imaging modalities'
name = 'impose'
year = "2020"



setup(
    name=name,
    author=author,
    author_email='dev@craban.de',
    url='',
    version="0.0.1",
    packages=find_packages(),
    package_dir={name: name},
    include_package_data=True,
    license="None",
    description=description,
    long_description=open('README.rst').read() if exists('README.rst') else '',
    install_requires=["czifile",
                      "h5py>=2.10.0",
                      "numpy>=1.17.0",
                      "pyqt5>=5.15.0",
                      "pyqtgraph==0.11.1",
                      "scikit-image>=0.17.2",
                      "imageio",  # open image files
                      ],
    setup_requires=["pytest-runner"],
    python_requires=">=3.6",
    tests_require=["pytest"],
    keywords=["image analysis", "biology", "microscopy"],
    classifiers=['Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Visualization',
                 'Intended Audience :: Science/Research',
                 ],
    platforms=['ALL'],
)
