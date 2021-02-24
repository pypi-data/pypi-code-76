# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interstate_py',
 'interstate_py.control',
 'interstate_py.error',
 'interstate_py.internalio',
 'interstate_py.reactive',
 'interstate_py.serialization',
 'interstate_py.zeromq']

package_data = \
{'': ['*']}

install_requires = \
['Rx>=3.1.0,<4.0.0',
 'aiozmq>=0.7.1,<0.8.0',
 'janus>=0.5.0,<0.6.0',
 'pyzmq>=18.0,<19.0']

entry_points = \
{'console_scripts': ['build = poetry_scripts:build',
                     'install = poetry_scripts:install',
                     'publish = poetry_scripts:publish',
                     'release = poetry_scripts:release',
                     'test = poetry_scripts:test']}

setup_kwargs = {
    'name': 'interstate-py',
    'version': '1.2.0',
    'description': '',
    'long_description': None,
    'author': 'LeftshiftOne Software GmbH',
    'author_email': 'devs@leftshift.one',
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
