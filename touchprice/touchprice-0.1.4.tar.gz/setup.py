# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['touchprice']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.22.0', 'shioaji>=0.3.1-dev8,<0.4.0']

setup_kwargs = {
    'name': 'touchprice',
    'version': '0.1.4',
    'description': 'shioaji touchprice extentions',
    'long_description': None,
    'author': 'Sally',
    'author_email': 'nipolikae@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
