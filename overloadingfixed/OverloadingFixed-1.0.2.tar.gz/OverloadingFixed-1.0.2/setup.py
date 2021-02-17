from itertools import takewhile
import os

from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = str.join('', takewhile(lambda l: not l.startswith('Installation'), f.readlines()[15:]))

setup(
    name = 'OverloadingFixed',
    version = '1.0.2',
    description = 'Function overloading for Python 3',
    long_description = '\n' + readme,
    url = 'https://github.com/toto112358/overloading.py',
    author = 'L. Pham-Trong',
    author_email = 'spam@lucasanss.xyz',
    license = 'MIT',
    py_modules = ['overloading'],
    install_requires = [],
    keywords = 'overload function method dispatch',
    classifiers = [
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License'
    ]
)
