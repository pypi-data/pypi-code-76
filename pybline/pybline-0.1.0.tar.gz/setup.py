#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='pybline',
    version='0.1.0',
    packages=find_packages(exclude=['.*tests.*']),
    entry_points={
        'console_scripts': [
            'pybline = pybline.gui:main',
        ],
    },
    install_requires=[
        'numpy',
        'numba',
        'pyrotd',
        'setuptools',
    ],
    test_suite='tests',
    author='Albert Kottke',
    author_email='albert.kottke@gmail.com',
    description='Python baseline correction.',
    license='MIT',
    long_description=readme,
    url='http://github.com/arkottke/pybline',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
    ], )
