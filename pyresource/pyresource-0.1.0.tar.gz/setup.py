# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyresource', 'pyresource.django', 'pyresource.utils']

package_data = \
{'': ['*']}

install_requires = \
['ttable>=0.6.3,<0.7.0']

setup_kwargs = {
    'name': 'pyresource',
    'version': '0.1.0',
    'description': 'Resource is an SDK for building declarative, feature-rich REST APIs',
    'long_description': None,
    'author': 'Anthony Leontiev',
    'author_email': 'ant@devlit.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aleontiev/pyresource',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
