# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_mk']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-mk',
    'version': '0.1.0',
    'description': 'A sample python package for week 1',
    'long_description': None,
    'author': 'Micah Kwok',
    'author_email': 'micahkwok@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
