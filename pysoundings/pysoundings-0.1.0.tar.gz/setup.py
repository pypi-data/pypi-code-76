# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysoundings']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'lxml>=4.6.2,<5.0.0',
 'pandas>=1.2.1,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pysoundings',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dkllrjr',
    'author_email': 'dg.kllr.jr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
