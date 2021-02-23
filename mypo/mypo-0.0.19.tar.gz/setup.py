# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypo']

package_data = \
{'': ['*']}

install_requires = \
['isort>=5.7.0,<6.0.0',
 'mypy>=0.812,<0.813',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'scipy>=1.6.0,<2.0.0',
 'yfinance>=0.1.55,<0.2.0']

setup_kwargs = {
    'name': 'mypo',
    'version': '0.0.19',
    'description': '',
    'long_description': '# mypo\n\n',
    'author': 'sonesuke',
    'author_email': 'iamsonesuke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sonesuke/mypo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.1,<4.0.0',
}


setup(**setup_kwargs)
