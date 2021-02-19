#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Otger Ballester'
__copyright__ = 'Copyright 2021'
__date__ = '19/2/21'
__credits__ = ['Otger Ballester', ]
__license__ = 'CC0 1.0 Universal'
__version__ = '0.1'
__maintainer__ = 'Otger Ballester'
__email__ = 'otger@ifae.es'

import os
from setuptools import setup, find_packages

# Read README and CHANGES files for the long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as fh:
      long_description = fh.read()

# print(find_packages(exclude=('tests',)))
setup(
      name="zmqcs",
      version="0.1.0",
      description="Client Server implementation made with zmq",
      long_description_content_type="text/markdown",
      long_description=long_description,
      install_requires=['pyzmq'],
      python_requires='>=3',
      provides=["zmqcs"],
      author="Otger Ballester",
      author_email="ifae-control@ifae.es",
      license="CC0 1.0 Universal",
      url="https://github.com/IFAEControl/zmqCS",
      zip_safe=False,
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3",
                  ],
      package_dir={'': 'src'},
      packages=find_packages(where=os.path.join('.', 'src'), exclude=('tests',))
)