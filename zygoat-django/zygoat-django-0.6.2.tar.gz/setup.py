# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zygoat_django',
 'zygoat_django.management',
 'zygoat_django.management.commands',
 'zygoat_django.middleware',
 'zygoat_django.settings']

package_data = \
{'': ['*']}

install_requires = \
['django-environ>=0.4.4,<0.5.0',
 'django-redis>=4.12.1,<5.0.0',
 'django>=2',
 'djangorestframework-camel-case>=1.2.0,<2.0.0',
 'djangorestframework>=3.9.1,<4.0.0',
 'importlib-metadata>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'zygoat-django',
    'version': '0.6.2',
    'description': '',
    'long_description': None,
    'author': 'Mark Rawls',
    'author_email': 'markrawls96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
