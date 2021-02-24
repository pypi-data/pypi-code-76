# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_rissangs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-rissangs',
    'version': '1.1.4',
    'description': 'Python package that eases the pain of concatenating Pandas categoricals.',
    'long_description': None,
    'author': 'rissangs',
    'author_email': '70673560+rissangs@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
