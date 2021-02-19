# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymoneroasync', 'pymoneroasync.models', 'pymoneroasync.models.daemon']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.1,<0.17.0',
 'pydantic>=1.7.3,<2.0.0',
 'sansio-jsonrpc>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'pymoneroasync',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'euri10',
    'author_email': 'benoit.barthelet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
