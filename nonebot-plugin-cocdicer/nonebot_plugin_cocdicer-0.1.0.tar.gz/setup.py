# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_cocdicer']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-alpha.10,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-cocdicer',
    'version': '0.1.0',
    'description': 'A COC dice plugin for Nonebot2',
    'long_description': None,
    'author': 'abrahumlink',
    'author_email': '307887491@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
