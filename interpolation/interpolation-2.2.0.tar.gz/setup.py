# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interpolation',
 'interpolation.multilinear',
 'interpolation.multilinear.tests',
 'interpolation.smolyak',
 'interpolation.smolyak.tests',
 'interpolation.splines',
 'interpolation.splines.tests',
 'interpolation.tests']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.47', 'numpy>=1.18.1', 'scipy>=1.4.1', 'tempita>=0.5.2']

setup_kwargs = {
    'name': 'interpolation',
    'version': '2.2.0',
    'description': 'Interpolation in Python',
    'long_description': '![CI](https://github.com/EconForge/interpolation.py/workflows/CI/badge.svg?branch=master) ![DOC](https://github.com/EconForge/interpolation.py/workflows/DOC/badge.svg?branch=master)\n\n\nSee the [doc](https://www.econforge.org/interpolation.py).\n',
    'author': 'Pablo Winant',
    'author_email': 'pablo.winant@gmail.com',
    'maintainer': 'Pablo Winant',
    'maintainer_email': 'pablo.winant@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
