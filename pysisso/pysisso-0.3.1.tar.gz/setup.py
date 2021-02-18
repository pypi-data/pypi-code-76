# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysisso', 'pysisso.tests']

package_data = \
{'': ['*']}

install_requires = \
['custodian>=2020.4.27,<2021.0.0',
 'monty>=3.0.4,<5',
 'pandas>=1.0.5,<2.0.0',
 'scikit-learn>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'pysisso',
    'version': '0.3.1',
    'description': 'Python interface to the SISSO (Sure Independence Screening and Sparsifying Operator) method.',
    'long_description': None,
    'author': 'David Waroquiers',
    'author_email': 'david.waroquiers@matgenix.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
