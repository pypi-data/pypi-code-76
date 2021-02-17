# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['strapp', 'strapp.click', 'strapp.flask', 'strapp.sqlalchemy']

package_data = \
{'': ['*']}

extras_require = \
{'click': ['click'],
 'click:python_version >= "3.6" and python_version < "3.7"': ['dataclasses'],
 'flask': ['flask', 'flask_reverse_proxy'],
 'flask:python_version >= "3.6" and python_version < "3.7"': ['dataclasses'],
 'sentry': ['sentry-sdk'],
 'sqlalchemy': ['sqlalchemy']}

setup_kwargs = {
    'name': 'strapp',
    'version': '0.2.4',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
