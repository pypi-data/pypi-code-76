# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_jk']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'pypkgs-jk',
    'version': '0.1.0',
    'description': 'Toy Python package for UBC DSCI 524',
    'long_description': None,
    'author': 'Junghoo Kim',
    'author_email': 'jkim222383@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
