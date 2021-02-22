"""
A collection of utilities used across multiple BIG projects
"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# read version from the VERSION file
# For a discussion on single-sourcing the version across setup.py and the
# project code, see https://packaging.python.org/en/latest/single_source_version.html
with open(os.path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

# get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='big-utils',
    version=version,
    description=__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/pgolec/big-utils',
    author='Patrick Golec',
    author_email='patrick.golec@bitsinglass.com',
    license="MIT License",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Systems Administration',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    # What does your project relate to?
    keywords='BIG common shared utilities helpers',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    python_requires='>=3.9.1, <4',
    install_requires=[
        'PyJWT>=2.0.1',
    ],
    project_urls={
        'Wiki': 'https://bitbucket.org/pgolec/big-utils/wiki',
        'Source': 'https://bitbucket.org/pgolec/big-utils/src',
    },
)
