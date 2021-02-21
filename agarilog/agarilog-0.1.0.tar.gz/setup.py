# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['agarilog', 'agarilog.handlers', 'agarilog.handlers.web']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.3,<4.0.0',
 'alog>=1.1.0,<2.0.0',
 'pydantic[dotenv]>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'agarilog',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'agari',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
