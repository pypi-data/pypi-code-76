# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xwire',
 'xwire.transport',
 'xwire.transport._private',
 'xwire.transport._private.csv',
 'xwire.transport._private.decorators',
 'xwire.transport._private.exceptions',
 'xwire.transport.public']

package_data = \
{'': ['*']}

install_requires = \
['xwire.common>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'xwire.transport',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'tylerlaberge',
    'author_email': 'tylerlaberge@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
