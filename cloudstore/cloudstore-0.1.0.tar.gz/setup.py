# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cloudstore']

package_data = \
{'': ['*'], 'cloudstore': ['data/*']}

install_requires = \
['azure-storage-blob>=12.7.1,<13.0.0',
 'boto3>=1.17.3,<2.0.0',
 'google-cloud-storage>=1.35.1,<2.0.0',
 'tqdm>=4.56.2,<5.0.0']

entry_points = \
{'console_scripts': ['haxo = cloudstore.console:cli']}

setup_kwargs = {
    'name': 'cloudstore',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'unrahul',
    'author_email': 'rahulunair@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
