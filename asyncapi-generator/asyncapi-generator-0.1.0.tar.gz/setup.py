# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncapi_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncapi-generator',
    'version': '0.1.0',
    'description': '',
    'long_description': '<h1 align="center">\n    <strong>asyncapi-generator</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/asyncapi-generator" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/asyncapi-generator" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/asyncapi-generator/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/asyncapi-generator">\n    <br />\n    <a href="https://pypi.org/project/asyncapi-generator" target="_blank">\n        <img src="https://img.shields.io/pypi/v/asyncapi-generator" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/asyncapi-generator">\n    <img src="https://img.shields.io/github/license/Kludex/asyncapi-generator">\n</p>\n\n\n## Installation\n\n``` bash\npip install asyncapi-generator\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/asyncapi-generator',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
