# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['btcpay_django', 'btcpay_django.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2', 'btcpay-python>=1.3.0,<2.0.0', 'django-crawfish>=0.0.8,<0.0.9']

setup_kwargs = {
    'name': 'btcpay-django',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Crawford Leeds',
    'author_email': 'crawford@crawfordleeds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
