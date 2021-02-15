# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commandfrog', 'commandfrog.drivers', 'commandfrog.operations']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'dephell>=0.8.3,<0.9.0',
 'loguru>=0.5.3,<0.6.0',
 'paramiko>=2.7.2,<3.0.0',
 'setuptools>=53.0.0,<54.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['build = build.__init__:build']}

setup_kwargs = {
    'name': 'commandfrog',
    'version': '0.3.1',
    'description': 'Infra',
    'long_description': None,
    'author': 'Andrew Magee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
