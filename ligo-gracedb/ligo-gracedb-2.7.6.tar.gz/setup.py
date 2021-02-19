# -*- coding: utf-8 -*-
# Copyright (C) Brian Moe, Branson Stephens (2015)
#
# This file is part of gracedb
#
# gracedb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gracedb.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys
from setuptools import setup, find_packages


def parse_version(path):
    """Extract the `__version__` string from the given file"""
    with open(path, 'r') as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get readme file for long_description
readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(readme_file, 'rb') as f:
    long_description = f.read().decode().strip()


# Required packages for tests
tests_require = []
# Add pytest requirement - 5.0.0+ only supports Python 3.5+
pytest_requirement = 'pytest>=3.1.0'
pyparsing_requirement = 'pyparsing==2.4.7'
zipp_requirement = 'zipp==0.6.0'
it_requirement = 'more-itertools==5.0.0'
if sys.version_info < (3, 5):
    pytest_requirement += ',<5.0.0'
tests_require.append(pytest_requirement)
tests_require.append(pyparsing_requirement)
tests_require.append(zipp_requirement)
tests_require.append(it_requirement)
tests_require.append('pytest-cov')

# Add mock for Python 2
if sys.version_info.major < 3:
    tests_require.append('mock==3.0.5')

# Only install setup_requires for the specific command being used
SETUP_REQUIRES = []
if 'test' in sys.argv:
    SETUP_REQUIRES.append('pytest-runner>=2.12')

# Classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    ('License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)'),
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Astronomy',
    'Topic :: Scientific/Engineering :: Physics',
]


###############################################################################
# Call setup() ################################################################
###############################################################################
setup(
    name="ligo-gracedb",
    version=parse_version(os.path.join('ligo', 'gracedb', 'version.py')),
    author=("Tanner Prestegard, Alexander Pace, Branson Stephens, Brian Moe, "
            "Patrick Brady"),
    author_email="tanner.prestegard@ligo.org, alexander.pace@ligo.org",
    description="A Python package for accessing the GraceDB API.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://git.ligo.org/lscsoft/gracedb-client",
    license='GPL-3.0-or-later',
    namespace_packages=['ligo'],
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    install_requires=['future>=0.15.0',
                      'six>=1.9.0',
                      'cryptography>=1.7.2, <=3.3.1',
                      'requests>=2.6.0',
                      ],
    setup_requires=SETUP_REQUIRES,
    tests_require=tests_require,
    package_data={
        'ligo.gracedb.test': [
            'integration/data/*',
        ],
    },
    entry_points={
        'console_scripts': [
            'gracedb=ligo.gracedb.cli.client:main',
            'gracedb_legacy=ligo.gracedb.legacy_cli:main',
        ],
    },
)
