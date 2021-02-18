# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['payfast_client']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2021.1,<2022.0', 'requests-futures>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'payfast-client',
    'version': '0.1.0',
    'description': 'Python client for interacting with the Payfast API',
    'long_description': None,
    'author': 'Fergus Strangways-Dixon',
    'author_email': 'fergusdixon101@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
