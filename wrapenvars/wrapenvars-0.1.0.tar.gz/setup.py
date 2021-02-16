# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wrapenvars']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wrapenvars',
    'version': '0.1.0',
    'description': 'encode/decode base64 strings',
    'long_description': '# WRAPENVARS\n\nencode/decode base64 strings.\n',
    'author': 'David Guerrero',
    'author_email': 'deivguerrero@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deivguerrero/wrapenvars',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
