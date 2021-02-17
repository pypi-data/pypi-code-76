# Copyright 2020 Software Factory Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from setuptools import setup, find_packages

my_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(my_dir, 'README.md')) as f:
    README = f.read()

with open(f'{my_dir}/requirements.txt') as file:
    REQUIRES = file.readlines()

with open(f'{my_dir}/requirements-dev.txt') as file:
    REQUIRES_DEV = file.readlines()

setup(
    name='yapsched',
    version='0.2.0',
    description='Yet Another Python Scheduler',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    author='Software Factory Labs',
    author_email='eric@softwarefactorylabs.com',
    packages=find_packages(include=['yapsched', 'yapsched.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    extras_require={
        'dev': REQUIRES_DEV,
    },
    python_requires='>= 3.7',
)
