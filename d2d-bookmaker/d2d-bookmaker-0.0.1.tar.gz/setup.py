# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bookmaker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'd2d-bookmaker',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Toby Nance',
    'author_email': 'toby.nance@draft2digital.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
