# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monotone_bipartition']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20,<21',
 'funcy>=1.14,<2.0',
 'lazytree>=0.3.1,<0.4.0',
 'lenses>=1.0.0,<2.0.0',
 'numpy>=1.19.1,<2.0.0']

setup_kwargs = {
    'name': 'monotone-bipartition',
    'version': '0.3.1',
    'description': 'Compute Monotone Threshold Surfaces and compute distances between surfaces.',
    'long_description': None,
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
