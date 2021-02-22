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
    'version': '0.1.0b2',
    'description': 'FastAPI-HyperModel is a FastAPI + Pydantic extension for simplifying hypermedia-driven API development. This module adds a new Pydantic model base-class, supporting dynamic `href` generation based on object data.',
    'long_description': None,
    'author': 'Joel Collins',
    'author_email': 'joel.collins@renalregistry.nhs.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jtc42/fastapi-hypermodel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
