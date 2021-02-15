# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pretty_poly']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['doctest = run_tests:run_doctest',
                     'test = run_tests:test']}

setup_kwargs = {
    'name': 'pretty-poly',
    'version': '0.2.0a3',
    'description': 'Display polyominos and polyomino tilings in various pretty formats.',
    'long_description': None,
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
