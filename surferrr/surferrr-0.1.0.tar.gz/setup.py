# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['surferrr', 'surferrr.base', 'surferrr.browser']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3']

setup_kwargs = {
    'name': 'surferrr',
    'version': '0.1.0',
    'description': 'Control web browser like a surfer.',
    'long_description': None,
    'author': 'Takeru Saito',
    'author_email': 'takelushi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
