# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virgo']

package_data = \
{'': ['*']}

install_requires = \
['ply>=3.11,<4.0']

setup_kwargs = {
    'name': 'pyvirgo',
    'version': '0.2.0a3',
    'description': 'A Python package for the Virgo language',
    'long_description': '# PyVirgo\n\nThis is a Python implementation of Virgo, the graph declarative language.\n\nYou can find details of Virgo with the Go implementation at https://github.com/r2d4/virgo\n\n',
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jwg4/pyvirgo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
