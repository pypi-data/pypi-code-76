# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurorax',
 'aurorax._internal',
 'aurorax.api',
 'aurorax.availability',
 'aurorax.ephemeris',
 'aurorax.metadata',
 'aurorax.requests',
 'aurorax.sources']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.4,<4.0.0',
 'humanize>=3.2.0,<4.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pyaurorax',
    'version': '0.4.4',
    'description': 'Python library for interacting with the AuroraX API',
    'long_description': None,
    'author': 'Darren Chaddock',
    'author_email': 'dchaddoc@ucalgary.ca',
    'maintainer': 'Darren Chaddock',
    'maintainer_email': 'dchaddoc@ucalgary.ca',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
