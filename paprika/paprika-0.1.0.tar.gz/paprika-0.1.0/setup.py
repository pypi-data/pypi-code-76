# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paprika']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'paprika',
    'version': '0.1.0',
    'description': 'Paprika is a python library that reduces boilerplate. Heavily inspired by Project Lombok.',
    'long_description': '# Paprika\nPaprika is a python library that reduces boilerplate. Heavily inspired by Project Lombok.\n',
    'author': 'Rayan Hatout',
    'author_email': 'rayan.hatout@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rayanht/paprika',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
