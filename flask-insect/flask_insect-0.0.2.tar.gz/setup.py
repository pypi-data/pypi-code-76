# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_insect']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2,<2.0.0', 'etcd3>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'flask-insect',
    'version': '0.0.2',
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
