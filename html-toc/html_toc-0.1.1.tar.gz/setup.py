# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['html_toc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'html-toc',
    'version': '0.1.1',
    'description': 'Generate TOC from HTML.',
    'long_description': '# html-toc\n\n**html-toc** is a simple tool based on the builtin `html.parser` module to generate table of content from HTML. See [`test.py`](html_toc/test.py) for usage.\n',
    'author': 'Richard Chien',
    'author_email': 'richardchienthebest@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/verilab/html-toc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
