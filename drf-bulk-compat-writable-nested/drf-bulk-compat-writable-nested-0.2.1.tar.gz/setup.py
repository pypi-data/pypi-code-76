#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from setuptools import find_packages, setup

from rest_framework_bulk import __version__, __author__


def read(fname):
    return (open(os.path.join(os.path.dirname(__file__), fname), 'rb')
            .read().decode('utf-8'))


authors = read('AUTHORS.rst')
history = read('HISTORY.rst').replace('.. :changelog:', '')
licence = read('LICENSE.rst')
readme = read('README.rst')

requirements = read('requirements.txt').splitlines() + [
    'setuptools',
]

test_requirements = (
    read('requirements.txt').splitlines()
    + read('requirements-dev.txt').splitlines()[1:]
)

setup(
    name='drf-bulk-compat-writable-nested',
    version=__version__,
    author=__author__,
    author_email='alex@mooloo.io',
    description='Django REST Framework bulk CRUD view mixins with compatibility for the writable nested serializers package "drf-writable-nested"',
    long_description='\n\n'.join([readme, history, authors, licence]),
    url='https://github.com/axmpda/django-rest-framework-bulk/tree/patch-2',
    license='MIT',
    keywords='django',
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
    ],
)
