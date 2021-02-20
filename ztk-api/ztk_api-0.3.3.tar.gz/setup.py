# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ztk_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4',
 'dataclasses-json>=0.5,<0.6',
 'pydantic>=1.7,<2',
 'requests>=2.25,<3',
 'structlog>=21,<22',
 'tbk_api>=0.2.1,<0.3']

setup_kwargs = {
    'name': 'ztk-api',
    'version': '0.3.3',
    'description': '折淘客接口',
    'long_description': '# 折淘客API\n\n![PyPI - Version](https://img.shields.io/pypi/v/ztk_api)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ztk_api)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/ztk_api)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/ztk_api)\n![GitHub repo size](https://img.shields.io/github/repo-size/qiyutechdev/ztk_api)\n![Lines of code](https://img.shields.io/tokei/lines/github/qiyutechdev/ztk_api)\n\n# WARNING(警告)\n\n这个项目已经不再维护，请使用 [QiYu API](https://github.com/QiYuTechDev/qiyu-api) 项目。\n\n# WARNING\n\n    this is only for internal use (use at your own risk)\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/QiYuTechDev/ztk_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
