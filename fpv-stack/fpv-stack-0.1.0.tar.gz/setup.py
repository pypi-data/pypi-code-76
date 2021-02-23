# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fpv_stack', 'fpv_stack.templates']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['fpv-stack = fpv_stack.main:fpv_stack']}

setup_kwargs = {
    'name': 'fpv-stack',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mikhail Cherdakov',
    'author_email': 'mishacherdakov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
