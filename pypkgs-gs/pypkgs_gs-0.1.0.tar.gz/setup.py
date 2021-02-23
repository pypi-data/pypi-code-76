# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_gs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-gs',
    'version': '0.1.0',
    'description': 'Python package that eases the pain of concatenating Pandas Categoricals!',
    'long_description': None,
    'author': 'Gurdeepak Sidhu',
    'author_email': 'gurdeepaksidhu@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
