# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_ch']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-ch',
    'version': '0.1.0',
    'description': 'individual assignment 1 - python package tutorial',
    'long_description': None,
    'author': 'deepcl',
    'author_email': 'hkcmul@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
