# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['html_toc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'html-toc',
    'version': '0.1.0',
    'description': 'Generate TOC from HTML.',
    'long_description': None,
    'author': 'Richard Chien',
    'author_email': 'richardchienthebest@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
