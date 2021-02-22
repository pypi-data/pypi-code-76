#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- file: setup.py -*-
# -*- purpose: -*-

'''
setup.py file for mcvariable module
'''

#from distutils.core import setup
from setuptools import setup

NAME = 'mcvariable'
VERSION = '0.1.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

    
setup(name=NAME,
      version=VERSION,
      packages=[NAME],
      description='Monte Carlo(random) Variable Object ',
      long_description = long_description,
      long_description_content_type = "text/markdown",
      author='Greg Henning',
      author_email='ghenning@iphc.cnrs.fr',
      url='https://gitlab.in2p3.fr/gregoire.henning/python-montecarlo-variable',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6',
      )
