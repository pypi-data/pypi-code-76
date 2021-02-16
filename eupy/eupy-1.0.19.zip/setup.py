#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup

setup(name = 'eupy',
      version = '1.0.19',
      description = 'Python set of utils and libraries',
      url = 'http://github.com/fivosts/eupy',
      author = 'Foivos Tsimpourlas',
      author_email = 'fivos_ts@hotmail.com',
      license = 'MIT',
      install_requires = [ "datetime",
                           "matplotlib",
                           "numpy",
                           "scrapy>=2.0.0",
                           "seaborn",
                           "pathlib",
                        ],
      packages = ['eupy', 'eupy.mrcrawley', 'eupy.native', 'eupy.hermes'],
      classifiers = [
                  "Programming Language :: Python :: 3.7",
               ]
      )
