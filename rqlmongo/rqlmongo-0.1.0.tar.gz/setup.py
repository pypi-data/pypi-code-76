# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rqlmongo']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=3.11.3,<4.0.0', 'pyrql>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'rqlmongo',
    'version': '0.1.0',
    'description': 'Resource Query Language for PyMongo',
    'long_description': '# RQLMongo\n\n[![Build Status](https://travis-ci.org/pjwerneck/rqlmongo.svg?branch=develop)](https://travis-ci.org/pjwerneck/rqlmongo)\n\nResource Query Language extension for PyMongo\n\n## Overview\n\nResource Query Language (RQL) is a query language designed for use in\nURIs, with object-style data structures.\n\nrqlmongo is an RQL extension for PyMongo. It translates an RQL query\nto a MongoDB aggregation pipeline that can be used to expose MongoDB\ncollections as an HTTP API endpoint and perform complex queries using\nonly querystring parameters.\n',
    'author': 'Pedro Werneck',
    'author_email': 'pjwerneck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pjwerneck/rqlmongo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
