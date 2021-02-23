# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3wm', 's3wm.layouts', 's3wm.tests', 's3wm_core']

package_data = \
{'': ['*']}

install_requires = \
['frozendict>=1.2,<2.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-xlib>=0.29,<0.30']

entry_points = \
{'console_scripts': ['s3wm = s3wm.main:main']}

setup_kwargs = {
    'name': 's3wm',
    'version': '0.1.0',
    'description': 'Simple Window manager.',
    'long_description': None,
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
