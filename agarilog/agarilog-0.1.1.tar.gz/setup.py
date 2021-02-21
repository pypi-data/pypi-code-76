# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['agarilog', 'agarilog.handlers', 'agarilog.handlers.web']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.3,<4.0.0', 'pydantic[dotenv]>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'agarilog',
    'version': '0.1.1',
    'description': 'simple logger for message services.',
    'long_description': None,
    'author': 'agari',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sakuv2/agarilog',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
