# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

setuptools.setup(
    name="ad_ci_tools",
    version='0.1.1',
    author="Rotaru Sergey",
    author_email="rsv@arenadata.io",
    description="Ci library with miscellaneous utils",
    url="https://github.com/arenadata/ci_tools",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'gitpython', 'wheel'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
