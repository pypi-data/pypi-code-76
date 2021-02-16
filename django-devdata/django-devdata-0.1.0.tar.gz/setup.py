# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['devdata', 'devdata.management', 'devdata.management.commands']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-devdata',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dan Palmer',
    'author_email': 'dan@danpalmer.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
