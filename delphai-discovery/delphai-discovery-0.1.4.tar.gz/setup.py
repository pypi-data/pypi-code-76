# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delphai_discovery']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-reflection>=1.35.0,<2.0.0',
 'grpcio>=1.35.0,<2.0.0',
 'httpx[http2]>=0.16.1,<0.17.0',
 'python-consul>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'delphai-discovery',
    'version': '0.1.4',
    'description': 'delphai microservice discovery',
    'long_description': None,
    'author': 'Barath Kumar',
    'author_email': 'barath@delphai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
