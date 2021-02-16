# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tablpy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib==3.2',
 'pandas>=1.2.2,<2.0.0',
 'scipy>=1.6.0,<2.0.0',
 'sympy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'tablpy',
    'version': '0.2.0',
    'description': 'A package that makes importing and handeling data',
    'long_description': '# Tablpy\nA python module that enables easy treatment of data  \n\nInstall it with\n\n> `pip install tablpy`\n',
    'author': 'AmdaUwU',
    'author_email': 'jbat2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AmdaUwU/tablpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
