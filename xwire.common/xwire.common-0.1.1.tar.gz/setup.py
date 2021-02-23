# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xwire',
 'xwire.common',
 'xwire.common._private',
 'xwire.common._private.env',
 'xwire.common._private.env.decorators',
 'xwire.common._private.utils',
 'xwire.common._private.utils.decorator_utils',
 'xwire.common.public']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xwire.common',
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
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
