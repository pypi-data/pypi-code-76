# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_ktan']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-ktan',
    'version': '0.1.0',
    'description': 'Individual assignment 1 Python package',
    'long_description': None,
    'author': 'tan95',
    'author_email': 'andrew--tan@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
