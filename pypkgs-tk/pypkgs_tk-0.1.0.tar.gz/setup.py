# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_tk']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-tk',
    'version': '0.1.0',
    'description': 'Python toy package to practice the process of making packages',
    'long_description': None,
    'author': 'Trevor Kinsey',
    'author_email': 'trevor_kinsey@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
