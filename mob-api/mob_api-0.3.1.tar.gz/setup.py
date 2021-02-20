# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mob_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4', 'pydes>=2,<3', 'requests>=2.24,<3', 'structlog>=21,<22']

setup_kwargs = {
    'name': 'mob-api',
    'version': '0.3.1',
    'description': 'mob api used by QiYuTech',
    'long_description': None,
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
