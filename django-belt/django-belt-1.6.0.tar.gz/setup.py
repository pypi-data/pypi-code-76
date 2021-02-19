# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['belt', 'belt.django_filters', 'belt.rest_framework']

package_data = \
{'': ['*']}

install_requires = \
['django-filter>=2.4.0,<3.0.0',
 'django-model-utils>=4.1.0,<5.0.0',
 'django>=3.0.7,<4.0.0',
 'djangorestframework>=3.12.2,<4.0.0']

setup_kwargs = {
    'name': 'django-belt',
    'version': '1.6.0',
    'description': 'Simple package with some utilities for Django.',
    'long_description': '===========\nDjango Belt\n===========\n\nSimple package with some utilities for Django.\n\n.. image:: https://travis-ci.org/marcosgabarda/django-belt.svg?branch=master\n    :target: https://travis-ci.org/marcosgabarda/django-belt\n\n.. image:: https://coveralls.io/repos/github/marcosgabarda/django-belt/badge.svg?branch=master\n    :target: https://coveralls.io/github/marcosgabarda/django-belt?branch=master\n\n\nQuick start\n-----------\n\n**1** Install using pip::\n\n    pip install django-belt\n\n**2** Add "belt" to your INSTALLED_APPS settings like this::\n\n    INSTALLED_APPS += (\'belt\',)\n\n',
    'author': 'Marcos Gabarda',
    'author_email': 'hey@marcosgabarda.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcosgabarda/django-belt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
