"""Minimal setup file"""

from setuptools import setup


setup(
    # package metadata
    name='meridian-test',
    version='4.2.42',
    description='Minimal Python package to illustrate best practices',
    #url='https://github.com',

    # package author(s)/maintainer(s) info
    author='Casey O\'Kane',
    author_email='casey.okane8451@gmail.com',

    # explicitly state directory where package source code is
    packages=['meridian-test'],

    # If set to True, this tells setuptools to automatically include any 
    # data files it finds inside your package directories that are specified 
    # by your MANIFEST.in file.
    include_package_data=True,

)
