# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cloud_drives']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'google-api-python-client>=1.12.8,<2.0.0',
 'google-auth-oauthlib>=0.4.2,<0.5.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'uvicorn>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'fastapi-cloud-drives',
    'version': '0.1.0',
    'description': 'Module for FastAPI to work with cloud drives',
    'long_description': None,
    'author': 'Hasan Aliyev',
    'author_email': 'hasan.aliyev.555@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
