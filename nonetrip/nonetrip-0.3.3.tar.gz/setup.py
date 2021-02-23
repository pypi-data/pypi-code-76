# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonetrip',
 'nonetrip.command',
 'nonetrip.command.argfilter',
 'nonetrip.compat',
 'nonetrip.experimental',
 'nonetrip.plugins']

package_data = \
{'': ['*']}

install_requires = \
['aiocache>=0.11.1,<0.12.0',
 'nonebot2>=2.0.0-alpha.10,<3.0.0',
 'singledispatchmethod>=1.0,<2.0']

extras_require = \
{'scheduler': ['APScheduler>=3.7.0,<4.0.0']}

setup_kwargs = {
    'name': 'nonetrip',
    'version': '0.3.3',
    'description': 'A compatibility layer plug-in on NoneBot2 which can provide compatibility with NoneBot1',
    'long_description': None,
    'author': 'mix',
    'author_email': 'admin@yami.im',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
