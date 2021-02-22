#
#  Python-music
#  Python music module.
#  Copyright Medilocus 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="python-music",
    version="0.0.2",
    author="Medilocus",
    author_email="huangpatrick16777216@gmail.com",
    description="Python music module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/medilocus/python-music",
    py_modules=["music"],
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)
