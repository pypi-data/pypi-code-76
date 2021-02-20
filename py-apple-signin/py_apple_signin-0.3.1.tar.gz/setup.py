# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_apple_signin']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4',
 'cryptography>=3.0,<4.0',
 'dataclasses-json>=0.5,<0.6',
 'pyjwt>=2.0,<3',
 'requests>=2.24,<3']

setup_kwargs = {
    'name': 'py-apple-signin',
    'version': '0.3.1',
    'description': 'Apple Sign In Python Server Side impl',
    'long_description': '# Apple SignIn SDK for Python\n\nApple SignIn Server Side in Python (with sync & async API)\n\n![PyPI - Version](https://img.shields.io/pypi/v/py-apple-signin)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-apple-signin)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/py_apple_signin)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/py-apple-signin)\n![GitHub repo size](https://img.shields.io/github/repo-size/qiyutechdev/py_apple_signin)\n![Lines of code](https://img.shields.io/tokei/lines/github/qiyutechdev/py_apple_signin)\n\n## WARING(警告)\n\nThis project is sunset, use [QiYuAPI](https://github.com/QiYuTechDev/qiyu-api) please.\n\n这个项目已经不在维护, 请使用 [QiYuAPI](https://github.com/QiYuTechDev/qiyu-api).\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/QiYuTechDev/py_apple_signin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
