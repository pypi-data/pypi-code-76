# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cry',
 'cry.eq',
 'cry.fields',
 'cry.py',
 'cry.py.anf',
 'cry.py.containers',
 'cry.py.tree',
 'cry.py.tree.node',
 'cry.py.utils',
 'cry.rsa',
 'cry.sbox2',
 'cry.sbox2.algorithms',
 'cry.sbox2.equiv',
 'cry.sbox2.generators',
 'cry.utils']

package_data = \
{'': ['*']}

install_requires = \
['bint>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'cry',
    'version': '0.2.1',
    'description': 'Cry: SageMath/Python Toolkit for Cryptanalytic Research',
    'long_description': '# Cry: SageMath/Python Toolkit for Cryptanalytic Research\n\nThis repository contains a bunch of various crypto-related algorithms implemented in Python 3 and SageMath. Pure Python code is located in cry/py package and can be imported from python code. The other modules must be imported from the SageMath interpreter.\n\nThe most significant part is formed by S-Box analysis algorithms, implemented in the cry.sbox2.SBox2 class, which is similar to from sage.crypto.SBox but is much more rich. Another cool S-Box library is [SboxU](https://github.com/lpp-crypto/sboxU) by Léo Perrin. It contains some more advanced algorithms, highly recommended!\n\n**WARNING:** This library is not well-shaped yet and many things (including API and structure) may change in future. For now, I will try to keep compatability only for minor versions. That is, lock to the minor version if you use this package.\n\n**NOTE** Before, this library was called *cryptools*, but since this name is used on PyPI, I decided to switch to *cry*, which is shorter.\n\nCurrently, there is no documentation but examples will be added soon.\n\n## Installation\n\n```bash\n# for SageMath\n$ sage pip install -U cry\n# for python3\n$ pip3 install -U cry\n```\n\nPrevious python2 version (cryptools) can be found in the tag *py2-arhived*.\n\n## Development\n\nFor development or building this repository, [poetry](https://python-poetry.org/) is needed.\n',
    'author': 'hellman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
