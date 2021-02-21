# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_rate_limiter']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'aio-rate-limiter',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jonathan Drake',
    'author_email': 'jdrake@narrativescience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
