# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_hypermodel']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'fastapi-hypermodel',
    'version': '0.1.0b1',
    'description': '',
    'long_description': None,
    'author': 'Joel Collins',
    'author_email': 'joel.collins@renalregistry.nhs.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
