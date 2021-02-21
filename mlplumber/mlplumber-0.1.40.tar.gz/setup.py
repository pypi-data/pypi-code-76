#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re

for line in open('mlplumber/__init__.py'):
    match = re.match('__version__ *= *"(.*)"', line)
    if match:
        __version__, = match.groups()


setup(name='mlplumber',
      version=__version__,
      description='ML Utilities for constructing pipeline',
      maintainer='Ritesh Agrawal',
      maintainer_email='ragrawal@gmail.com',
      url='https://github.com/ragrawal/mlplumber',
      packages=['mlplumber'],
      keywords=['scikit', 'sklearn', 'pandas', 'baikal'],
      setup_requires=['flake8'],
      install_requires=[
          'sklearn-pandas>=2.0.0',
          'baikal>=0.4.1'
      ],     
      tests_require=['pytest']
      )
