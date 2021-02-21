# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['depending']

package_data = \
{'': ['*']}

install_requires = \
['astunparse>=1.6.3,<2.0.0', 'redbaron>=0.9.2,<0.10.0']

setup_kwargs = {
    'name': 'depending',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Blake',
    'author_email': 'blakeinvictoria@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
