#!/usr/bin/env python

import os
from setuptools import setup


# Utility function to read the README file.
# https://pythonhosted.org/an_example_pypi_project/setuptools.html#setting-up-setup-py
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='netflix-blocklist-test',
    version='0.2.0',
    description='Empty package to occupy the namespace on PyPI.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Netflix',
    author_email='netflix-atlas@googlegroups.com',
    license='Apache 2.0',
    url='https://github.com/Netflix/blocklist-test/',
    packages=['blocklisttest'],
    install_requires=[],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
