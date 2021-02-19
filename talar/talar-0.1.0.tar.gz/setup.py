# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['talar', 'talar.client', 'talar.resources', 'talar.resources.tests']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'talar',
    'version': '0.1.0',
    'description': 'Python library for the Talar API',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
