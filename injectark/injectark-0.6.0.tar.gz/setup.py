# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['injectark']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'injectark',
    'version': '0.6.0',
    'description': 'Dependency Injector for Python',
    'long_description': None,
    'author': 'eecheverry',
    'author_email': 'eecheverry@nubark.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
