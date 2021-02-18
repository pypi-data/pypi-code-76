# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sinusboard', 'sinusboard.client', 'sinusboard.server']

package_data = \
{'': ['*'],
 'sinusboard.server': ['static/*',
                       'static/css/*',
                       'static/images/*',
                       'static/js/*',
                       'templates/*']}

install_requires = \
['Flask>=1.1.2,<2.0.0',
 'gunicorn>=20.0.4,<21.0.0',
 'requests>=2.25.1,<3.0.0',
 'whitenoise>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'sinusboard',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
