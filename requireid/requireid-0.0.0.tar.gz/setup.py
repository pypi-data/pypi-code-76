# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requireid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'requireid',
    'version': '0.0.0',
    'description': 'under development',
    'long_description': '# python package in development\n\n*More info soon.*\n\n\n## Installation with `pip`\nLike you would install any other Python package, use `pip`, `poetry`, `pipenv` or your weapon of choice.\n```\n$ pip install <package>\n```\n\n\n## Usage and examples\n\n#### Use-case\n',
    'author': 'Carl Oscar Aaro',
    'author_email': 'hello@carloscar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kalaspuff',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
