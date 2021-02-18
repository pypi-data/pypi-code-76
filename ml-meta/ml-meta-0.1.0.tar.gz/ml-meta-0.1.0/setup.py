# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_meta']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ml-meta',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Seth Woodworth',
    'author_email': 'seth@sethish.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
