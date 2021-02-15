# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia', 'graia.component']

package_data = \
{'': ['*']}

install_requires = \
['graia-application-mirai', 'graia-broadcast>=0.7.0']

setup_kwargs = {
    'name': 'graia-component-selector',
    'version': '0.0.6',
    'description': '',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': 'GreyElaina@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
