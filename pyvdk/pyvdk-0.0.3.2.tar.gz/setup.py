# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvdk',
 'pyvdk.api',
 'pyvdk.api.categories',
 'pyvdk.event',
 'pyvdk.rules',
 'pyvdk.tools',
 'pyvdk.tools.keyboard',
 'pyvdk.types']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'vbml>=1.1,<2.0']

setup_kwargs = {
    'name': 'pyvdk',
    'version': '0.0.3.2',
    'description': 'VK toolkit',
    'long_description': '# pyVDK\n[![PyPI version](https://badge.fury.io/py/pyvdk.svg)](https://badge.fury.io/py/pyvdk)\n![PyPI downloads per mounth](https://img.shields.io/pypi/dm/pyvdk)\n[![Documentation Status](https://readthedocs.org/projects/pyvdk/badge/?version=latest)](https://pyvdk.readthedocs.io/ru/latest/?badge=latest)\n[![VK chat](https://img.shields.io/badge/VK%20chat-support-blueviolet)](https://vk.me/join/AJQ1d/RAzBm4QcrxZ5hJTFSJ)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/UT1C/pyvdk)\n\n## Установка\nУстановить pyvdk можно напрямую с PyPI:\n```\npip install pyvdk\n```\n\n## Фичи\n- void; // (for now)\n\n## TODO list\n\n- [x] Категории в апи\n- [ ] Покрытие типами\n- [ ] Обработка всех событий\n- [ ] ? Юзер\n',
    'author': 'lightmanLP',
    'author_email': 'liteman1000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
