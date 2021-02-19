# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fivetran']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fivetran',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Michael Cooper',
    'author_email': 'macoop2363@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
