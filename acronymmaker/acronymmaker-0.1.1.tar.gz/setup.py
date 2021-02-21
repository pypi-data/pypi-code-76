##############################################################################
#                                                                            #
#   AcronymMaker - Create awesome acronyms for your projects!                #
#   Copyright (c) 2020-2021 - Romain Wallon (romain.gael.wallon@gmail.com)   #
#                                                                            #
#   This program is free software: you can redistribute it and/or modify     #
#   it under the terms of the GNU General Public License as published by     #
#   the Free Software Foundation, either version 3 of the License, or        #
#   (at your option) any later version.                                      #
#                                                                            #
#   This program is distributed in the hope that it will be useful,          #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                     #
#   See the GNU General Public License for more details.                     #
#                                                                            #
#   You should have received a copy of the GNU General Public License        #
#   along with this program.                                                 #
#   If not, see <https://www.gnu.org/licenses/>.                             #
#                                                                            #
##############################################################################


"""
Setup script for deploying AcronymMaker on PyPI and installing it using pip.
"""


from setuptools import setup

import acronymmaker


def readme() -> str:
    """
    Reads the README.md file of the project to use its content as a long
    description of the package.

    :return: The long description of AcronymMaker.
    """
    with open('README.md') as file:
        return file.read()


setup(
      name=acronymmaker.__name__,
      version=acronymmaker.__version__,
      packages=[acronymmaker.__name__],
      scripts=['bin/acronymmaker'],

      description=acronymmaker.__summary__,
      long_description=readme(),
      long_description_content_type='text/markdown',
      keywords=acronymmaker.__keywords__,
      url=acronymmaker.__uri__,

      author=acronymmaker.__author__,
      author_email=acronymmaker.__email__,

      install_requires=[
          "hopcroftkarp>=1.2.5",
          "pyfiglet>=0.8.post1"
      ],

      test_suite='nose.collector',
      tests_require=[
          'coverage',
          'nose'
      ],

      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Operating System :: OS Independent'
      ],
      license=acronymmaker.__license__,

      include_package_data=True,
      zip_safe=False
)
