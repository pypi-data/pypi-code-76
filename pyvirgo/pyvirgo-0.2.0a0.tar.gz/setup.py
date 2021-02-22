# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virgo']

package_data = \
{'': ['*']}

install_requires = \
['ply>=3.11,<4.0']

setup_kwargs = {
    'name': 'pyvirgo',
    'version': '0.2.0a0',
    'description': 'A Python package for the Virgo language',
    'long_description': None,
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
