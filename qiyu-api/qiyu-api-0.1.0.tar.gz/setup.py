# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qiyu_api',
 'qiyu_api.apns_sdk_py',
 'qiyu_api.mob_api',
 'qiyu_api.py_apple_signin',
 'qiyu_api.ztk_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4',
 'cryptography>=3.0,<4.0',
 'dataclasses-json>=0.5,<0.6',
 'pydantic>=1.7,<2',
 'pydes>=2,<3',
 'pyjwt>=2.0,<3',
 'requests>=2.25,<3',
 'structlog>=21,<22',
 'tbk_api>=0.2.1,<0.3']

setup_kwargs = {
    'name': 'qiyu-api',
    'version': '0.1.0',
    'description': '奇遇科技 Python API 合集',
    'long_description': '# QiYu-api\n\n[![Black Format Check](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/black-format.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/black-format.yml)\n[![CodeQL](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/codeql-analysis.yml)\n[![Poetry Publish](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/poetry_pypi.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/poetry_pypi.yml)\n[![Pylama Lint](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/pylama-lint.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/pylama-lint.yml)\n[![pytest](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/pytest.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/pytest.yml)\n\n奇遇科技 Python API 集合\n\n## 当前已经合并\n\n* ztk_api\n* mob_api\n* apns_sdk_py\n* py_apple_signin\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://oss.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
