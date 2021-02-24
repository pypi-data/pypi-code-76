# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykagskangbolu']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pykagskangbolu',
    'version': '0.1.0',
    'description': 'A starter package for python packaging',
    'long_description': None,
    'author': 'KangboLu',
    'author_email': 'kblu@ucdavis.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
