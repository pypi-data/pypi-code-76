#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup, find_packages


with open(pathlib.Path(__file__).parent / 'README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='pytadolog',
      version='0.1.1',
      description='CSV logger for PyTado from Josh Gibson',
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords=['tado', 'python', 'logging'],
      author='Josh Gibson',
      author_email='josh-gibson@outlook.com',
      url='https://github.com/jjgibson/PyTadoLog',
      python_requires='>=3.6',
      install_requires=[
        'keyring',
        'numpy',
        'openpyxl',
        'pandas',
      ],
      license='MIT',
      platforms=['any'],
      packages=find_packages(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Home Automation',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
      ],
      entry_points ={ 
        'console_scripts': [ 
          'tadolog = pytadolog.__main__:main'
        ]
      },
      scripts=['scripts/csv2excel'],
      zip_safe=False,
)
