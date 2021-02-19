# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['super_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'super-py',
    'version': '0.4.0',
    'description': 'Features that Python should have in the standard library',
    'long_description': '# SuperPy\n\n[![Downloads](https://pepy.tech/badge/super-py)](https://pepy.tech/project/super-py)\n[![Downloads](https://pepy.tech/badge/super-py/month)](https://pepy.tech/project/super-py)\n[![Downloads](https://pepy.tech/badge/super-py/week)](https://pepy.tech/project/super-py)\n\nShould be pretty self explanatory.\nThere are 5 sub modules:\n- sp.concurrency\n- sp.dicts\n- sp.disk\n- sp.logging\n- sp.string\n- sp.testing\n\nEach module contains documented functions that provide useful extra functionalities, that probably should have been in the standard library all along.',
    'author': 'Marcel Kröker',
    'author_email': 'kroeker.marcel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkrd/SuperPy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
