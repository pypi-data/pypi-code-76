# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynautobot', 'pynautobot.core', 'pynautobot.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'pynautobot',
    'version': '1.0.0a1',
    'description': 'Nautbot API client library',
    'long_description': None,
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/pynautobot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
