# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lk_utils', 'lk_utils.resource.metadata']

package_data = \
{'': ['*'],
 'lk_utils': ['resource/*'],
 'lk_utils.resource.metadata': ['more/*']}

install_requires = \
['lk-logger>=3.6,<4.0', 'xlrd==1.2', 'xlsxwriter>=1.3,<2.0']

setup_kwargs = {
    'name': 'lk-utils',
    'version': '1.4.4',
    'description': 'LK Utils is made for data processing.',
    'long_description': None,
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
