#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
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
#
from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cyclonefw',
    version='1.0.9',
    description='A package to simplify the creation of MAX models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wenlaizhou/cyclonefw',
    author='CODAIT',
    author_email='',
    license='Apache',
    packages=['cyclonefw', 'cyclonefw.core', 'cyclonefw.model', 'cyclonefw.utils'],
    zip_safe=True,
    install_requires=[
        'requests',
        'flask-restplus',
        'flask-restx==0.1.1',
        'flask-cors==3.0.9',
        'Pillow==7.2.0',
        'numpy==1.19.1',
    ],
    test_suite='nose.collector',
    tests_require=['nose']
)
