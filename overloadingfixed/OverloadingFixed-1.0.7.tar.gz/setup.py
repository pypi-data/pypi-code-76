from itertools import takewhile
import os

import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = str.join('', takewhile(lambda l: not l.startswith('Installation'), f.readlines()[15:]))

setuptools.setup(
    name = 'OverloadingFixed',
    version = '1.0.7',
    author="L. Pham-Trong",
    author_email="spam@lucasanss.xyz",
    description="Function overloading for Python 3",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/toto112358/overloading.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
