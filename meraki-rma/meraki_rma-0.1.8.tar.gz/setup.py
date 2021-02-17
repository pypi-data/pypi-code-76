# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meraki_rma']

package_data = \
{'': ['*']}

install_requires = \
['meraki-dashboard-connect>=0.1.1,<0.2.0',
 'meraki-env>=0.1.1,<0.2.0',
 'meraki-exception>=0.1.0,<0.2.0',
 'meraki>=1.4.3,<2.0.0',
 'rich>=9.10.0,<10.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'meraki-rma',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Thomas Christory',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
