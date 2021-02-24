# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_crh']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-crh',
    'version': '0.1.0',
    'description': 'Python package for individual assignment 1 of dsci 524',
    'long_description': None,
    'author': 'Cameron Harris',
    'author_email': 'camharris22@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
