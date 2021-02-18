# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import fileinput
from setuptools import setup, find_packages


__author__ = ["Christoph Schimeczek", "Ulrich Frey", "Marc Deissenroth-Uhrig", "Benjamin Fuchs", "Felix Nitsch"]
__copyright__ = "Copyright 2021, German Aerospace Center (DLR)"

__license__ = "Apache License 2.0"
__maintainer__ = "Felix Nitsch"
__email__ = "fame@dlr.de"
__status__ = "Production"


PACKAGE_DIR = "src/main/python/fameprotobuf/"


def readme():
    with open('README.md') as f:
        return f.read()


def generate_init():
    """Generates an empty `__init__.py` file in the `fameprotobuf` folder and passes if already existent"""
    try:
        file = open(PACKAGE_DIR + "__init__.py", "x")
        file.close()
    except FileExistsError:
        pass


def adapt_imports():
    """Changes imports in fameprotobuf from `import ...` to `from fameprotobuf import ...`"""
    for file_name in os.listdir(PACKAGE_DIR):
        with fileinput.FileInput(os.path.join(PACKAGE_DIR, file_name), inplace=True) as file:
            for line in file:
                if "import" in line and "_pb2" in line and "from fameprotobuf" not in line:
                    line = line.replace("import", "from fameprotobuf import")
                print(line, end='')


if __name__ == '__main__':
    generate_init()
    adapt_imports()

    setup(name='fameprotobuf',
          version='1.1.1',
          description='Protobuf definitions converted to python classes for use in `fameio`',
          keywords=['FAME', 'agent-based modelling', 'fameio'],
          url='https://gitlab.com/fame-framework/fame-protobuf/',
          author=', '.join(__author__),
          author_email=__email__,
          license=__license__,
          package_dir={'': 'src/main/python'},
          packages=find_packages(where='src/main/python'),
          classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: Apache Software License",
                "Operating System :: OS Independent",
          ],
          install_requires=['protobuf'],
          zip_safe=False,
          python_requires='>=3.6',
          )
