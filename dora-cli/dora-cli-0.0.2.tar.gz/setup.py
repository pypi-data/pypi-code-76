# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dora_cli']

package_data = \
{'': ['*']}

install_requires = \
['clint>=0.5.1,<0.6.0',
 'docker>=4.4.2,<5.0.0',
 'docopt>=0.6.2,<0.7.0',
 'esdk-obs-python>=3.20.11,<4.0.0',
 'huaweicloud-sdk-python>=1.0.28,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'dora-cli',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'didone',
    'author_email': 'didone@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
