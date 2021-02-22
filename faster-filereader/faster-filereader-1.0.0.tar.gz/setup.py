#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Wed Dec 11 11:42:29 CET 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: setup.py -*-
# -*- purpose: -*-
 
'''
Module docstring
'''
from setuptools import setup

NAME = 'faster-filereader'
VERSION = '1.0.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name=NAME,
      version=VERSION,
      packages=['faster', 'faster.dataunpackers'],
      package_data={'faster': ['test/*.fast']},
      description='Python faster system file reader',
      long_description=long_description,
      long_description_content_type="text/markdown", 
      author='Greg Henning',
      author_email='ghenning@iphc.cnrs.fr',
      url='https://gitlab.in2p3.fr/gregoire.henning/faster',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6',
      )
