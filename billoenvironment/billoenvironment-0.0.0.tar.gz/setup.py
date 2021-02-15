# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['billoenvironment']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'billoenvironment',
    'version': '0.0.0',
    'description': 'internal use',
    'long_description': '# internal use',
    'author': 'Billogram',
    'author_email': 'platform@billogram.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/billogram',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
