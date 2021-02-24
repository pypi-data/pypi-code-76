# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toy_python_package']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'toy-python-package',
    'version': '0.1.0',
    'description': 'A Toy Python Package',
    'long_description': None,
    'author': 'Heidi Ye',
    'author_email': 'heidiye@students.ubc.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
