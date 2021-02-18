#!/usr/bin/env python
from json import load
from os import system
from setuptools import setup
from sys import argv

metadata = load(open('metadata.json'))

if argv[-1] == 'publish':
    system('python setup.py sdist bdist_wheel')
    system('twine upload dist/*')
    exit()

with open('README.md', encoding='utf-8') as file:
    readme = file.read()

setup(
    long_description=readme,
    **metadata
)
