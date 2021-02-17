# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gimme_db_token']

package_data = \
{'': ['*']}

install_requires = \
['awscli>=1.18.194,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'cryptography>=3.1,<4.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['gimme_db_token = gimme_db_token.__main__:run']}

setup_kwargs = {
    'name': 'cyral-gimme-db-token',
    'version': '0.4.0',
    'description': 'Eases using Cyral for SSO login to databases.',
    'long_description': None,
    'author': 'Cyral',
    'author_email': 'dgado@cyral.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
