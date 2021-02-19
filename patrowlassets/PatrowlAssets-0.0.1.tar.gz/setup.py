#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup file."""
from setuptools import setup, find_packages
import os
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# automatically captured required modules for install_requires in requirements.txt
with open(os.path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]

dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name='PatrowlAssets',
    version='0.0.1',
    description='Python API and CLI for extracting assets from Cloud and virtualized systems',
    url='https://github.com/Patrowl/PatrowlAssets',
    author='Nicolas Mattiocco',
    author_email='nicolas@patrowl.io',
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    keyword="patrowl, patrowlhears, cve, vuln, vulnerabilities, security, nvd, exploit, poc, secops",
    dependency_links=dependency_links,
    entry_points='''
        [console_scripts]
        hears=patrowlassets.cli:main
    ''',
    python_requires='>=3.6',
)
