# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apns_sdk_py']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4.0', 'dataclasses-json>=0.5,<0.6', 'requests>=2.25,<3']

setup_kwargs = {
    'name': 'apns-sdk-py',
    'version': '0.5.2',
    'description': 'QiYuTech APNs API Python SDK',
    'long_description': '# apns_sdk_py\n\nPython SDK for APNs API\n\n[Pypi](https://pypi.org/project/apns-sdk-py)\n\n## WARNING 警告\n\nThis Project is sunset, use [QiYuAPI](https://github.com/QiYuTechDev/qiyu-api) instead (all function have merged into)\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/QiYuTechDev/apns_sdk_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
