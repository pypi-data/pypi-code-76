# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_524_ind1']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-524-ind1',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'yzr96',
    'author_email': 'eric.yu@usask.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
