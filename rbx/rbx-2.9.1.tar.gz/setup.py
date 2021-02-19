# Copyright 2020 Rockabox Media Limited
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

from setuptools import find_packages, setup

setup(
    name='rbx',
    version='2.9.1',
    license='Apache 2.0',
    description='Scoota Platform utilities',
    long_description='A collection of common tools for Scoota services.',
    url='http://scoota.com/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
    ],
    author='The Scoota Engineering Team',
    author_email='engineering@scoota.com',
    python_requires='>=3.7',
    install_requires=[
        'arrow>=0.16',
        'Click<8',
        'colorama',
        'google-api-core>=1.22,<1.23',
        'google-cloud-firestore>=1.8.1,<2',
        'google-cloud-logging>=1.15,<2',
        'google-cloud-pubsub>=1.7,<2',
        'grpcio>=1.29.0,<2.0dev',
        'PyYAML>=5.1.2',
        'requests>=1.21.1',
    ],
    extras_require={
        'buildtools': [
            'bumpversion==0.5.3',
            'check-manifest',
            'fabric~=2.5.0',
            'twine',
        ],
        'eds': [
            'google-cloud-bigquery>=1.26,<2',
            'google-cloud-datastore>=1.15,<2',
            'PyMySQL',
            'rfc3339',
            'sqlalchemy>=1.3,<1.4',
        ],
        'geo': [
            'googlemaps>=4.4.2,<5',
        ],
        'mysql': [
            'PyMySQL',
            'sqlalchemy>=1.3,<1.4',
        ],
        'queues': [
            'rq==1.4.3',
            'rq-scheduler==0.10.0',
        ],
        'storage': [
            'google-cloud-storage>=1.31,<2',
        ],
        'tasks': [
            'google-cloud-tasks>=2.0,<3',
        ],
        'tests': [
            'Flask==1.1.2',
            'googlemaps>=4.4.2,<5',
        ],
    },
    entry_points={
        'console_scripts': [
            'buildtools = rbx.buildtools.cli:program.run [buildtools]',
            'geocode = rbx.geo.cli:geocode [geo]',
            'reverse_geocode = rbx.geo.cli:reverse_geocode [geo]',
            'unpack = rbx.geo.cli:unpack [geo]',
        ],
    },
    packages=find_packages(),
    zip_safe=True
)
