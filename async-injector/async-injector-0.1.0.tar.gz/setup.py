# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_injector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-injector',
    'version': '0.1.0',
    'description': 'Dependency injector for modern Python',
    'long_description': None,
    'author': 'Marcin Baczyński',
    'author_email': 'dev@mail.of.ninja',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
