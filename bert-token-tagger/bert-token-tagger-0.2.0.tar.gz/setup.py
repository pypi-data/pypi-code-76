# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bert_token_tagger']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.7.1,<2.0.0', 'transformers>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'bert-token-tagger',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'melisa-qordoba',
    'author_email': 'melisa@qordoba.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Qordobacode/library.bert.token.tagger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
