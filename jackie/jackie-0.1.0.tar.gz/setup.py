# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jackie', 'jackie.http', 'jackie.router']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.3.1,<4.0.0']

setup_kwargs = {
    'name': 'jackie',
    'version': '0.1.0',
    'description': 'A minimal ASGI web framework.',
    'long_description': None,
    'author': 'Daan van der Kallen',
    'author_email': 'mail@daanvdk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
