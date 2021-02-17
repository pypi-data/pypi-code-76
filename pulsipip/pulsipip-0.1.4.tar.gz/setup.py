# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pulsipip']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.5,<2.0.0', 'piphyperd>=1.9.10,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ppip = pulsipip.cli:main']}

setup_kwargs = {
    'name': 'pulsipip',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'catethos',
    'author_email': 'cloverethos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
