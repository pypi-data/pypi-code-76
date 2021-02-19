# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['base_client_api', 'base_client_api.models']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'aiohttp>=3.7.3,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'python-rapidjson>=1.0,<2.0',
 'tenacity>=6.3.1,<7.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'base-client-api',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Jerod Gawne',
    'author_email': 'jerodgawne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
