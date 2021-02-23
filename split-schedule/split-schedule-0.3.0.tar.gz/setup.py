# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['split_schedule']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.5,<4.0.0', 'pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'split-schedule',
    'version': '0.3.0',
    'description': 'Split schedule into smaller class sizes',
    'long_description': None,
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
