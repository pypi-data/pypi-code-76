#!/usr/bin/env python

from distutils.core import setup
from os.path import dirname
import sys

setup(
    name='ansible-collection-test-utils',
    version='0.1.0',
    description='Repackage the mock folder from ansible/tests for use in collection tests',
    author='Kay-Uwe (Kiwi) Lorenz',
    author_email='tabkiwi@gmail.com',
    install_requires=[ ],
    url='https://github.com/klorenz/ansilbe-collection-test-utils',
    packages=[
        'ansible_collection_test_utils', 
        'ansible_collection_test_utils.mock', 
    ],
    include_package_data = True,

    license="GPLv3+",
    )
