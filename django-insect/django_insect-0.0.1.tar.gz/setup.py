# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_insect']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.0,<4.0.0', 'etcd3>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'django-insect',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'pskishere',
    'author_email': 'pskishere@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
