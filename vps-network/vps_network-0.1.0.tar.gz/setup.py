# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vps_network',
 'vps_network.vps_ping',
 'vps_network.vps_speedtest',
 'vps_network.vps_traceroute']

package_data = \
{'': ['*']}

install_requires = \
['click>=7,<8',
 'icmplib>=2.0,<3',
 'pydantic>=1.7,<2.0',
 'requests>=2.25,<3',
 'rich>=9.11,<10',
 'speedtest-cli>=2.1,<3']

setup_kwargs = {
    'name': 'vps-network',
    'version': '0.1.0',
    'description': 'VPS Network Speed Test',
    'long_description': None,
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
