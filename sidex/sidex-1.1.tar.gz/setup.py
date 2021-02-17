#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from setuptools import setup, find_packages, Extension
import os,sys,re


with open('README.md', 'r') as fd:
  version = '1.1'
  author = 'Ryou Ohsawa'
  email = 'ohsawa@ioa.s.u-tokyo.ac.jp'
  description = 'SIDEX: Simple Data Exchange server over HTTP'
  long_description = fd.read()
  license = 'MIT'


classifiers = [
  'Development Status :: 3 - Alpha',
  'Environment :: Console',
  'Intended Audience :: Science/Research',
  'License :: OSI Approved :: MIT License',
  'Operating System :: POSIX :: Linux',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.7']


if __name__ == '__main__':

  setup(
    name='sidex',
    version=version,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/ryou_ohsawa/sidex/src/master/',
    license=license,
    packages=find_packages(),
    classifiers=classifiers,
    install_requires=['flask','requests',])
