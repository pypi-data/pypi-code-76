# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weasel_client',
 'weasel_client.raw_results',
 'weasel_client.resources',
 'weasel_client.scripts']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'weasel-client',
    'version': '0.0.1',
    'description': '`weasel-client` is a python library to access the `weasel-api`.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
