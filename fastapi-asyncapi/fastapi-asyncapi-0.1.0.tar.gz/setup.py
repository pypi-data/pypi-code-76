# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_asyncapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fastapi-asyncapi',
    'version': '0.1.0',
    'description': '',
    'long_description': '<h1 align="center">\n    <strong>fastapi-asyncapi</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/fastapi-asyncapi" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/fastapi-asyncapi" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/fastapi-asyncapi/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/fastapi-asyncapi">\n    <br />\n    <a href="https://pypi.org/project/fastapi-asyncapi" target="_blank">\n        <img src="https://img.shields.io/pypi/v/fastapi-asyncapi" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/fastapi-asyncapi">\n    <img src="https://img.shields.io/github/license/Kludex/fastapi-asyncapi">\n</p>\n\n\n## Installation\n\n``` bash\npip install fastapi-asyncapi\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/fastapi-asyncapi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
