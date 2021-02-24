# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_lhabashy']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-lhabashy',
    'version': '0.1.0',
    'description': 'Python package for assignment 1',
    'long_description': None,
    'author': 'larahabashy',
    'author_email': 'laraahabashy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
