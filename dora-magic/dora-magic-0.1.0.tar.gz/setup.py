# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dora_magic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dora-magic',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'didone',
    'author_email': 'didone@compasso.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
