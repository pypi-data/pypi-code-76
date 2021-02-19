# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages, Command

import logging

logger = logging.getLogger(__name__)

version = '0.1'


def do_setup():
    setup(
        name='smartstatic',
        description='smartchart static files',
        license='Apache License 2.0',
        version=version,
        packages=['smart_chart',],
        include_package_data=True,
        zip_safe=False,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.9',
        ],
        author='JohnYan',
        author_email='84345999@qq.com',
        url='https://www.smartchart.cn/',
        download_url=(
            'https://www.smartchart.cn/'),
        python_requires='>=3.6',
    )


if __name__ == "__main__":
    do_setup()
